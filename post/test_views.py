from django.test import TestCase
from django.urls import reverse
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from post.models import Post, Comment, ImageTags, ImageTagRelationships
from profile_page.models import ImageBoard
from post.forms import CommentForm
from cloudinary.models import CloudinaryField
from uuid import uuid4
from unittest.mock import patch
from django.utils.timezone import now

class PostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(username="testuser", password="password123")
        
        # Mock the CloudinaryField's validation during tests
        with patch.object(CloudinaryField, 'validate', return_value=None):
            # Create 15 test posts
            for i in range(15):
                Post.objects.create(
                    id=uuid4(),
                    title=f"Post {i+1}",
                    user=cls.user,
                    image="mock_image_url",  # This bypasses Cloudinary validation during tests
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
            Post.objects.all().order_by("-created_on")[:10],  # Explicitly order by "id"
            transform=lambda x: x
    )

    def test_paginator_object_in_context(self):
        """Test if the paginator object is included in the context."""
        response = self.client.get(reverse("home"))
        self.assertTrue("paginator" in response.context)
        self.assertIsInstance(response.context["paginator"], Paginator)

    def test_no_posts(self):
        """Test the view when there are no posts."""
        Post.objects.all().delete()  # Clear all posts
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


class PostDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.user = User.objects.create_user(username="testuser", password="password123")
        cls.other_user = User.objects.create_user(username="otheruser", password="password456")

        # Create a test post
        cls.post = Post.objects.create(
            id=uuid4(),
            title="Test Post",
            user=cls.user,
            image="mock_image_url",
            description="This is a test post.",
            created_on=now(),
        )

        # Create comments for the post
        cls.comment1 = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            body="This is the first comment.",
            created_on=now(),
        )
        cls.comment2 = Comment.objects.create(
            post=cls.post,
            author=cls.other_user,
            body="This is the second comment.",
            created_on=now(),
        )

        # Create tags for the post
        cls.tag1 = ImageTags.objects.create(tag_name="tag1")
        cls.tag2 = ImageTags.objects.create(tag_name="tag2")
        ImageTagRelationships.objects.create(post_id=cls.post, tag_name=cls.tag1)
        ImageTagRelationships.objects.create(post_id=cls.post, tag_name=cls.tag2)

        # Create boards for the user
        cls.board1 = ImageBoard.objects.create(user=cls.user, title="Test Board 1")
        cls.board2 = ImageBoard.objects.create(user=cls.user, title="Test Board 2")

    def test_view_url_exists_at_desired_location(self):
        """Test if the view is accessible by its URL."""
        response = self.client.get(reverse("post_detail", kwargs={"id": self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test if the correct template is used."""
        response = self.client.get(reverse("post_detail", kwargs={"id": self.post.id}))
        self.assertTemplateUsed(response, "post/post_details.html")

    def test_view_returns_correct_post(self):
        """Test if the correct post is returned in the context."""
        response = self.client.get(reverse("post_detail", kwargs={"id": self.post.id}))
        self.assertEqual(response.context["post"], self.post)

    def test_view_returns_correct_comments(self):
        """Test if the comments associated with the post are returned."""
        response = self.client.get(reverse("post_detail", kwargs={"id": self.post.id}))
        self.assertQuerySetEqual(
            response.context["comments"],
            [self.comment1, self.comment2],
            transform=lambda x: x,
        )

    def test_comment_ordering(self):
        """Test if comments are ordered by creation date."""
        response = self.client.get(reverse("post_detail", kwargs={"id": self.post.id}))
        comments = response.context["comments"]
        self.assertEqual(list(comments), [self.comment1, self.comment2])

    def test_view_returns_correct_comment_count(self):
        """Test if the correct number of comments is returned."""
        response = self.client.get(reverse("post_detail", kwargs={"id": self.post.id}))
        self.assertEqual(response.context["comment_count"], 2)

    def test_view_returns_tags(self):
        """Test if the tags associated with the post are returned."""
        response = self.client.get(reverse("post_detail", kwargs={"id": self.post.id}))
        self.assertQuerySetEqual(
            response.context["tags"].order_by("tag_name"),  # Ensure consistent ordering
            ImageTags.objects.filter(image_tag__post_id=self.post).order_by("tag_name"),
            transform=lambda x: x,
        )

    def test_view_returns_comment_form(self):
        """Test if a blank comment form is returned in the context."""
        response = self.client.get(reverse("post_detail", kwargs={"id": self.post.id}))
        self.assertIsInstance(response.context["comment_form"], CommentForm)

    def test_authenticated_user_boards(self):
        """Test if boards are returned for authenticated users."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("post_detail", kwargs={"id": self.post.id}))
        self.assertQuerySetEqual(
            response.context["user_boards"].order_by("id"),  # Ensure consistent ordering
            ImageBoard.objects.filter(user=self.user).order_by("id"),
            transform=lambda x: x,
        )

    def test_unauthenticated_user_boards(self):
        """Test if no boards are returned for unauthenticated users."""
        response = self.client.get(reverse("post_detail", kwargs={"id": self.post.id}))
        self.assertEqual(response.context["user_boards"], [])

    def test_invalid_post_id(self):
        """Test if a 404 is raised for an invalid post ID."""
        invalid_id = uuid4()  # Generate a random UUID
        response = self.client.get(reverse("post_detail", kwargs={"id": invalid_id}))
        self.assertEqual(response.status_code, 404)