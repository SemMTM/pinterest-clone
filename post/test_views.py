from django.test import TestCase
from django.urls import reverse
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from post.models import Post, Comment, ImageTags, ImageTagRelationships
from django.core.files.uploadedfile import SimpleUploadedFile
from profile_page.models import ImageBoard
from post.forms import CommentForm, PostForm
from cloudinary.models import CloudinaryField
from uuid import uuid4
from unittest.mock import patch
from django.utils.timezone import now
import json

class PostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(username="testuser", password="password123")
        
        # Mock the CloudinaryField's validation during tests
        with patch.object(CloudinaryField, 'validate', return_value=None):
            for i in range(15):
                Post.objects.create(
                    id=uuid4(),
                    title=f"Post {i+1}",
                    user=cls.user,
                    image="mock_image_url",  
                    description="Test description",
                )

    def test_view_url_exists_at_desired_location(self):
        """Test if the view is accessible by its URL."""
        response = self.client.get(reverse("home")) 
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test if the view is accessible using its name."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_correct_template_used_for_standard_request(self):
        """Test if the correct template is used for a non-HTMX request."""
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "post/index.html")

    def test_correct_template_used_for_htmx_request(self):
        """Test if the correct template is used for an HTMX request."""
        response = self.client.get(
            reverse("home"), HTTP_HX_REQUEST="true"
        )
        self.assertTemplateUsed(response, "post/image_list.html")

    def test_pagination_functionality(self):
        """Test if pagination works correctly and the correct number of items is shown."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["userimages"]), 10)  # First page should have 10 items

        # Test second page
        response = self.client.get(reverse("home") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["userimages"]), 5)  # Second page should have 5 items

    def test_invalid_page_raises_404(self):
        """Test that requesting an invalid page number raises a 404 error."""
        response = self.client.get(reverse("home") + "?page=9999")
        self.assertEqual(response.status_code, 404)

    def test_get_queryset_returns_correct_data(self):
        """Test that get_queryset returns the correct data."""
        response = self.client.get(reverse("home"))
        self.assertEqual(len(response.context["userimages"]), 10)
        self.assertQuerySetEqual(
            response.context["userimages"], 
            Post.objects.all().order_by("-created_on")[:10],  
            transform=lambda x: x
    )

    def test_paginator_object_in_context(self):
        """Test if the paginator object is included in the context."""
        response = self.client.get(reverse("home"))
        self.assertTrue("paginator" in response.context)
        self.assertIsInstance(response.context["paginator"], Paginator)

    def test_no_posts(self):
        """Test the view when there are no posts."""
        Post.objects.all().delete()  
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['userimages']), 0)
        self.assertTemplateUsed(response, 'post/index.html')

        # Check if the grid for posts is empty
        self.assertContains(response, 'class="image-grid"', msg_prefix="Grid container missing")

    def test_pagination_with_ordering(self):
        """Test pagination with posts ordered by -created_on."""
        response = self.client.get(reverse("home") + "?page=2")
        
        # Ensure the second page contains the correct posts
        second_page_posts = Post.objects.order_by("-created_on")[10:20]
        for post in second_page_posts:
            self.assertContains(response, post.title)

        # Ensure posts from the first page are not included
        first_page_posts = Post.objects.order_by("-created_on")[:10]
        for post in first_page_posts:
            self.assertNotContains(response, post.title)


class CreatePostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password123")
        cls.url = reverse("create_post")

        cls.valid_image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )

        cls.tag_clothes = ImageTags.objects.create(tag_name="clothes")
        cls.tag_art = ImageTags.objects.create(tag_name="art")

        cls.valid_data = {
            "title": "Test Post",
            "description": "This is a test description.",
            "tags": [cls.tag_clothes.pk, cls.tag_art.pk],  
            "image": cls.valid_image,
        }
        cls.invalid_data = {
            "title": "",  
            "description": "This description lacks an image.",
        }

    def test_create_post_get_request(self):
        """Test that the view renders the form for a GET request."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post/post_create.html")
        self.assertIsInstance(response.context["post_form"], PostForm)

    @patch("cloudinary.uploader.upload", return_value={
        "url": "http://mock.url/test_image.jpg",
        "public_id": "mock_public_id",
        "version": "1234567890",
        "type": "upload",
        "format": "jpg",
        "resource_type": "image"  
    })
    def test_create_post_valid_post_request(self, mock_upload):
        """Test that a valid POST request creates a post and returns success."""
        self.client.login(username="testuser", password="password123")

        data = self.valid_data.copy()

        response = self.client.post(self.url, data, follow=True)

        # Assert that the post was created
        self.assertEqual(Post.objects.count(), 1, "Post was not created!")
        post = Post.objects.first()
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.description, "This is a test description.")
        self.assertEqual(post.user, self.user)

        # Assert that tags were created and linked
        self.assertTrue(ImageTagRelationships.objects.filter(post_id=post, tag_name__tag_name="clothes").exists())
        self.assertTrue(ImageTagRelationships.objects.filter(post_id=post, tag_name__tag_name="art").exists())

        # Assert JSON response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)
        self.assertEqual(response.json()["message"], "Your post has been created successfully!")

    @patch("cloudinary.uploader.upload", return_value={
        "url": "http://mock.url/test_image.jpg",
        "public_id": "mock_public_id",
        "version": "1234567890",
        "type": "upload",
        "format": "jpg",
        "resource_type": "image" 
    })
    def test_create_post_without_tags(self, mock_upload):
        """Test that a valid POST request without tags still creates a post."""
        self.client.login(username="testuser", password="password123")

        data = self.valid_data.copy()
        data.pop("tags")  # Remove tags

        response = self.client.post(self.url, data, follow=True)

        # Assert that the post was created without tags
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(ImageTagRelationships.objects.filter(post_id=post).count(), 0)

        # Assert JSON response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)

    def test_create_post_invalid_post_request(self):
        """Test that an invalid POST request returns errors and does not create a post."""
        self.client.login(username="testuser", password="password123")

        response = self.client.post(self.url, self.invalid_data, content_type="application/json")

        # Assert that no post was created
        self.assertEqual(Post.objects.count(), 0)

        # Assert JSON response with errors
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["success"], False)
        self.assertIn("error", response.json())

    @patch("cloudinary.uploader.upload", return_value={
        "url": "http://mock.url/test_image.jpg",
        "public_id": "mock_public_id",
        "version": "1234567890",
        "type": "upload",
        "format": "jpg",
        "resource_type": "image"  
    })
    def test_create_post_missing_image(self, mock_upload):
        """Test that a POST request without an image is invalid."""
        self.client.login(username="testuser", password="password123")

        data = self.valid_data.copy()
        data.pop("image", None)  
        response = self.client.post(self.url, data, follow=True)

        # Assert that no post was created
        self.assertEqual(Post.objects.count(), 0)

        # Assert JSON response with errors
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["success"], False)
        self.assertIn("image", json.loads(response.json()["error"]))


class TagSuggestionsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ImageTags.objects.create(tag_name="clothes")
        ImageTags.objects.create(tag_name="art")
        ImageTags.objects.create(tag_name="artistic")
        ImageTags.objects.create(tag_name="abstract")
        ImageTags.objects.create(tag_name="nature")
        ImageTags.objects.create(tag_name="animals")
        ImageTags.objects.create(tag_name="fashion")
        ImageTags.objects.create(tag_name="travel")
        ImageTags.objects.create(tag_name="architecture")
        ImageTags.objects.create(tag_name="interior")
        ImageTags.objects.create(tag_name="food")
        ImageTags.objects.create(tag_name="photography")
        ImageTags.objects.create(tag_name="adventure")
        ImageTags.objects.create(tag_name="assets")
        ImageTags.objects.create(tag_name="action")
        ImageTags.objects.create(tag_name="activities") 

        cls.url = reverse("tag_suggestions")  

    def test_no_query_returns_all_tags(self):
        """Test that all tags are returned when no query is provided."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 10)  # Should return 10 tags
        tag_names = [tag["tag_name"] for tag in data]
        self.assertIn("clothes", tag_names)
        self.assertIn("art", tag_names)

    def test_query_matches_tags(self):
        """Test that the query matches and returns the correct tags."""
        response = self.client.get(self.url + "?q=art")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        tag_names = [tag["tag_name"] for tag in data]

        # Assert that the expected matches are returned
        expected_matches = ["art", "artistic"]
        for match in expected_matches:
            self.assertIn(match, tag_names)

    def test_query_with_partial_match(self):
        """Test that partial matches are returned correctly."""
        response = self.client.get(self.url, {"q": "a"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 10)  # Should return up to 10 matches
        tag_names = [tag["tag_name"] for tag in data]
        self.assertIn("art", tag_names)
        self.assertIn("animals", tag_names)
        self.assertIn("architecture", tag_names)

    def test_query_no_results(self):
        """Test that no results are returned when no tags match the query."""
        response = self.client.get(self.url, {"q": "nonexistent"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)  # No matches should return an empty list

    def test_query_limit_results(self):
        """Test that the number of results is limited to 10."""
        response = self.client.get(self.url, {"q": ""})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 10)  # Only 10 results should be returned

    def test_query_is_case_insensitive(self):
        """Test that the query is case-insensitive."""
        response = self.client.get(self.url + "?q=ART")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        tag_names = [tag["tag_name"] for tag in data]

        # Assert that the results include expected matches
        expected_matches = ["art", "artistic"]
        for match in expected_matches:
            self.assertIn(match, tag_names)

    def test_invalid_method_returns_error(self):
        """Test that methods other than GET return an error."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)  # Method not allowed


class AddCommentViewTest(TestCase):
    @classmethod
    @patch("cloudinary.uploader.upload", return_value={
            "url": "http://mock.url/test_image.jpg", 
            "public_id": "mock_public_id",
            "version": "1234567890",
            "type": "upload",
            "format": "jpg",
            "resource_type": "image"
            })
    def setUpTestData(cls, mock_upload):
        cls.user = User.objects.create_user(username="testuser", password="password123")
        
        # Create a test post
        cls.post = Post.objects.create(
            title="Test Post",
            description="Test Description",
            user=cls.user,
            image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
        )

        cls.url = reverse("add_comment", kwargs={"post_id": cls.post.id})

    def setUp(self):
        self.client.login(username="testuser", password="password123")

    
    @patch('django.utils.timezone.now', return_value=now())
    def test_add_valid_comment(self, mock_now):
        """Test adding a valid comment via AJAX."""
        data = {"body": "This is a test comment."}

        response = self.client.post(
            self.url,
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',  # Simulate AJAX request
        )

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)
        self.assertEqual(response.json()["body"], "This is a test comment.")
        self.assertEqual(response.json()["author"], self.user.username)

        # Check the comment in the database
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.body, "This is a test comment.")
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)

    def test_add_invalid_comment(self):
        """Test adding a comment with invalid form data."""
        data = {"body": ""}  # Empty body

        response = self.client.post(
            self.url,
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',  # Simulate AJAX request
        )

        # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid form data")

        # Assert no comment was created
        self.assertEqual(Comment.objects.count(), 0)

    def test_non_ajax_request(self):
        """Test the view returns an error for non-AJAX requests."""
        data = {"body": "This is a test comment."}

        response = self.client.post(self.url, data)

        # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid request")

        # Assert no comment was created
        self.assertEqual(Comment.objects.count(), 0)

    def test_anonymous_user(self):
        """Test that an anonymous user cannot add a comment."""
        self.client.logout()
        response = self.client.post(
            self.url,
            {"body": "Anonymous test comment"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 302)  
        expected_url = reverse("custom_accounts:login_modal")  
        self.assertTrue(response.url.startswith(expected_url))

        # Assert no comment was created
        self.assertEqual(Comment.objects.count(), 0)

    def test_invalid_post_id(self):
        """Test the view returns an error for an invalid post ID."""
        invalid_post_id = uuid4()  
        response = self.client.post(
            reverse("add_comment", kwargs={"post_id": invalid_post_id}),
            {"body": "Test comment on invalid post"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 404)

    def test_edge_case_body(self):
        """Test adding a comment with edge case data."""
        data = {"body": "A" * 600}  # Maximum length body

        response = self.client.post(
            self.url,
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',  # Simulate AJAX request
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)

        # Check the comment in the database
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.body, "A" * 600)


class CommentDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="user1", password="password123")
        cls.user2 = User.objects.create_user(username="user2", password="password123")
        cls.post = Post.objects.create(
            title="Test Post",
            description="Test Description",
            user=cls.user1,
        )
        cls.comment1 = Comment.objects.create(
            post=cls.post, author=cls.user1, body="Comment by user1"
        )
        cls.comment2 = Comment.objects.create(
            post=cls.post, author=cls.user2, body="Comment by user2"
        )
        cls.comment1_url = reverse(
            "delete_comment", kwargs={"post_id": cls.post.id, "comment_id": cls.comment1.id}
        )
        cls.comment2_url = reverse(
            "delete_comment", kwargs={"post_id": cls.post.id, "comment_id": cls.comment2.id}
        )

    def test_delete_own_comment(self):
        """Test that a user can delete their own comment."""
        self.client.login(username="user1", password="password123")
        response = self.client.post(self.comment1_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(id=self.comment1.id).exists())

    def test_post_owner_deletes_other_user_comment(self):
        """Test that the post owner can delete another user's comment."""
        self.client.login(username="user1", password="password123")
        response = self.client.post(self.comment2_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(id=self.comment2.id).exists())

    def test_user_cannot_delete_other_user_comment(self):
        """Test that a user cannot delete a comment they don't own (and they're not the post owner)."""
        self.client.login(username="user2", password="password123")
        response = self.client.post(self.comment1_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(id=self.comment1.id).exists())

    def test_anonymous_user_cannot_delete_comment(self):
        """Test that an anonymous user cannot delete a comment."""
        response = self.client.post(self.comment1_url)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(
            response.url.startswith(reverse("custom_accounts:login_modal"))
        )  

    def test_invalid_post_id(self):
        """Test that an invalid post ID returns a 404."""
        invalid_post_id = str(uuid4())
        invalid_url = reverse(
            "delete_comment", kwargs={"post_id": invalid_post_id, "comment_id": self.comment1.id}
        )
        self.client.login(username="user1", password="password123")
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, 404)

    def test_invalid_comment_id(self):
        """Test that an invalid comment ID returns a 404."""
        invalid_url = reverse(
            "delete_comment", kwargs={"post_id": self.post.id, "comment_id": 9999}
        )
        self.client.login(username="user1", password="password123")
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, 404)