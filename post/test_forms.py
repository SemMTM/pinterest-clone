from unittest.mock import patch
from django.test import TestCase
from post.forms import CommentForm, PostForm
from post.models import Comment, Post, ImageTags
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


class CommentFormTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="password123")
        # Create a post
        self.post = Post.objects.create(
            title="Test Post",
            user=self.user,
            image="test_image.jpg",
            description="Test description",
        )

    def test_form_initialization(self):
        """Test that the form initializes with the correct widget attributes."""
        form = CommentForm()
        self.assertEqual(form.fields['body'].widget.attrs['placeholder'], 'Add a comment')
        self.assertEqual(form.fields['body'].widget.attrs['rows'], '2')

    def test_form_valid_data(self):
        """Test that the form is valid with proper data."""
        form = CommentForm(data={"body": "This is a test comment."})
        self.assertTrue(form.is_valid())

        # Save the comment with the associated post
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.post  # Associate with the post
            comment.author = self.user  # Associate with the user
            comment.save()

            self.assertEqual(Comment.objects.count(), 1)
            self.assertEqual(comment.body, "This is a test comment.")

    def test_form_with_long_body(self):
        """Test that the form accepts a very long comment within the limit."""
        long_body = "a" * 600  # Exactly 600 characters
        form = CommentForm(data={"body": long_body})
        self.assertTrue(form.is_valid())

        # Save the comment with the associated post
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.post  # Associate with the post
            comment.author = self.user  # Associate with the user
            comment.save()

            self.assertEqual(Comment.objects.count(), 1)
            self.assertEqual(comment.body, long_body)

    def test_form_body_exceeds_max_length(self):
        """Test that the form is invalid when the comment exceeds 600 characters."""
        long_body = "a" * 601  # 601 characters
        form = CommentForm(data={"body": long_body})
        self.assertFalse(form.is_valid())
        self.assertIn("body", form.errors)
        self.assertEqual(form.errors["body"][0], "Ensure this value has at most 600 characters (it has 601).")

    def test_form_empty_body(self):
        """Test that the form is invalid when the body is empty."""
        form = CommentForm(data={"body": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("body", form.errors)
        self.assertEqual(form.errors["body"][0], "This field is required.")


class PostFormTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="password123")
        # Create sample tags
        self.tag1 = ImageTags.objects.create(tag_name="nature")
        self.tag2 = ImageTags.objects.create(tag_name="travel")
        self.tag3 = ImageTags.objects.create(tag_name="technology")
        self.tag4 = ImageTags.objects.create(tag_name="health")

    @patch("cloudinary.uploader.upload")
    def test_form_valid_data(self, mock_upload):
        """Test that the form is valid with proper data."""
        # Mock Cloudinary response
        mock_upload.return_value = {
            "url": "http://example.com/test_image.jpg",
            "public_id": "test_image",
            "version": "12345",
            "type": "upload",
            "format": "jpg",
            "resource_type": "image",
        }

        image = SimpleUploadedFile("test_image.jpg", b"fake_image_content", content_type="image/jpeg")
        form_data = {
            "title": "A test post",
            "description": "This is a description.",
            "tags": [self.tag1.pk, self.tag2.pk],
        }
        form_files = {"image": image}

        form = PostForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())
        post = form.save(commit=False)
        post.user = self.user
        post.save()

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.title, "A test post")
        self.assertEqual(post.description, "This is a description.")

    @patch("cloudinary.uploader.upload")
    def test_form_with_no_tags(self, mock_upload):
        """Test that the form is valid when no tags are selected."""
        # Mock Cloudinary response
        mock_upload.return_value = {
            "url": "http://example.com/test_image.jpg",
            "public_id": "test_image",
            "version": "12345",
            "type": "upload",
            "format": "jpg",
            "resource_type": "image",
        }

        image = SimpleUploadedFile("test_image.jpg", b"fake_image_content", content_type="image/jpeg")
        form_data = {
            "title": "A post without tags",
            "description": "No tags for this post.",
            "tags": [],
        }
        form_files = {"image": image}

        form = PostForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())
        post = form.save(commit=False)
        post.user = self.user
        post.save()

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.title, "A post without tags")

    def test_form_with_max_tags(self):
        """Test that the form is valid when selecting exactly 3 tags."""
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        form_data = {
            "title": "A test post with max tags",
            "description": "This is a post with exactly 3 tags.",
            "tags": [self.tag1.pk, self.tag2.pk, self.tag3.pk],
        }
        form_files = {"image": image}

        form = PostForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())

    @patch("cloudinary.uploader.upload")
    def test_form_exceeding_tag_limit(self, mock_upload):
        """Test that the form is invalid when selecting more than 3 tags."""
        # Mock Cloudinary response
        mock_upload.return_value = {
            "url": "http://example.com/test_image.jpg",
            "public_id": "test_image",
            "version": "12345",
            "type": "upload",
            "format": "jpg",
            "resource_type": "image",
        }

        image = SimpleUploadedFile("test_image.jpg", b"fake_image_content", content_type="image/jpeg")
        form_data = {
            "title": "A post with too many tags",
            "description": "Trying to select 4 tags.",
            "tags": [self.tag1.pk, self.tag2.pk, self.tag3.pk, self.tag4.pk],
        }
        form_files = {"image": image}

        form = PostForm(data=form_data, files=form_files)
        self.assertFalse(form.is_valid())
        self.assertIn("tags", form.errors)
        self.assertEqual(form.errors["tags"][0], "You can select a maximum of 3 tags.")

    def test_form_missing_image(self):
        """Test that the form is invalid when the image is missing."""
        form_data = {
            "title": "A post without an image",
            "description": "Missing the image file.",
            "tags": [self.tag1.pk],
        }

        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("image", form.errors)
        self.assertEqual(form.errors["image"][0], "No file selected!")

    def test_form_missing_title(self):
        """Test that the form is invalid when the title is missing."""
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        form_data = {
            "description": "This is a post without a title.",
            "tags": [self.tag1.pk],
        }
        form_files = {"image": image}

        form = PostForm(data=form_data, files=form_files)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertEqual(form.errors["title"][0], "This field is required.")

    def test_form_missing_description(self):
        """Test that the form is valid when the description is missing."""
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        form_data = {
            "title": "A post without description",
            "tags": [self.tag1.pk],
        }
        form_files = {"image": image}

        form = PostForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())