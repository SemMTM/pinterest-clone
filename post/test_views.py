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

        # Create valid tags
        cls.tag_clothes = ImageTags.objects.create(tag_name="clothes")
        cls.tag_art = ImageTags.objects.create(tag_name="art")

        cls.valid_data = {
            "title": "Test Post",
            "description": "This is a test description.",
            "tags": [cls.tag_clothes.pk, cls.tag_art.pk],  # Use valid tag primary keys
            "image": cls.valid_image,
        }
        cls.invalid_data = {
            "title": "",  # Title is required
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
        "resource_type": "image"  # Added the missing field
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
        "resource_type": "image"  # Added the missing field
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
        "resource_type": "image"  # Added the missing field
    })
    def test_create_post_missing_image(self, mock_upload):
        """Test that a POST request without an image is invalid."""
        self.client.login(username="testuser", password="password123")

        data = self.valid_data.copy()
        data.pop("image", None)  # Safely remove image
        response = self.client.post(self.url, data, follow=True)

        # Assert that no post was created
        self.assertEqual(Post.objects.count(), 0)

        # Assert JSON response with errors
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["success"], False)
        self.assertIn("image", json.loads(response.json()["error"]))