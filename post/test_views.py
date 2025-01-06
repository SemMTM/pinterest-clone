from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from uuid import uuid4
from post.models import Post, Comment, ImageTags, ImageTagRelationships
from post.forms import PostForm
from unittest.mock import patch
from profile_page.models import ImageBoard
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from django.utils.timezone import now
import json


class PostListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpassword")
        # Create multiple posts to test pagination
        for i in range(10):
            Post.objects.create(
                title=f"Test Post {i}",
                user=cls.user,
                likes=0,
            )

    def test_post_list_view_status_code(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_template_used(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "post/index.html")

    def test_post_list_view_pagination(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("userimages", response.context)
        self.assertEqual(len(response.context["userimages"]), 3)  # Paginate by 3

    def test_post_list_view_pagination_next_page(self):
        response = self.client.get(reverse("home") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertIn("userimages", response.context)
        self.assertEqual(len(response.context["userimages"]), 3)  # Second page has 3 posts

    def test_post_list_view_htmx_template(self):
        response = self.client.get(reverse("home"), HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post/image_list.html")


class PostDetailViewTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create a post
        self.post = Post.objects.create(
            title="Test Post",
            user=self.user,
            description="Test description",
            likes=0,
        )

        # Create comments
        self.comment1 = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="First comment"
        )
        self.comment2 = Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Second comment"
        )

        # Create user boards
        self.board = ImageBoard.objects.create(
            user=self.user,
            title="Test Board"  # Correct field for ImageBoard
        )

    def test_post_detail_view_status_code(self):
        """Test that the post_detail view returns a 200 status code for a valid post."""
        url = reverse('post_detail', args=[str(self.post.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_template_used(self):
        """Test that the correct template is used in the post_detail view."""
        url = reverse('post_detail', args=[str(self.post.id)])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "post/post_details.html")

    def test_post_detail_view_context_data(self):
        """Test that the post_detail view includes the correct context data."""
        self.client.login(username='testuser', password='password')
        url = reverse('post_detail', args=[str(self.post.id)])
        response = self.client.get(url)
        
        self.assertEqual(response.context['post'], self.post)
        self.assertEqual(list(response.context['comments']), [self.comment2, self.comment1])  # Ordered by -created_on
        self.assertEqual(response.context['comment_count'], 2)
        self.assertEqual(response.context['user_boards'][0], self.board)
        self.assertTrue(response.context['comment_form'])

    def test_post_detail_view_invalid_post(self):
        """Test that the post_detail view returns a 404 for an invalid post ID."""
        invalid_uuid = uuid4()
        url = reverse('post_detail', args=[str(invalid_uuid)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_detail_view_anonymous_user(self):
        """Test that an anonymous user can still access the post_detail view."""
        url = reverse('post_detail', args=[str(self.post.id)])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user_boards'], [])


class CreatePostViewTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        # Create tags
        self.tag1 = ImageTags.objects.create(tag_name="tag1")
        self.tag2 = ImageTags.objects.create(tag_name="tag2")

        # Set the URL for the create post view
        self.url = reverse("create_post")

        # Prepare invalid data (missing image)
        self.invalid_data = {
            "description": "This is a test post with invalid data.",
        }

    def test_create_post_get_request_authenticated(self):
        """Test that a GET request renders the form for authenticated users."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post/post_create.html")
        self.assertIn("post_form", response.context)

    def test_create_post_post_request_valid_data(self):
        """Test that a valid POST request creates a post and associated tags."""
        valid_image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x00\x00\x01\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3B",
            content_type="image/jpeg",
        )
        data = {
            "description": "This is a test post.",
            "tags": [self.tag1.tag_name, self.tag2.tag_name],
        }
        files = {"image": valid_image}

        response = self.client.post(self.url, {**data, **files}, follow=True)

        # Debugging
        form_errors = response.context["post_form"].errors
        print("Form Errors:", form_errors)

        # Assert that a post is created
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertIsNone(post.title, "")
        self.assertEqual(post.description, data["description"])
        self.assertEqual(post.user, self.user)

        # Assert that tags are associated with the post
        self.assertEqual(ImageTagRelationships.objects.count(), 2)
        tags = ImageTagRelationships.objects.filter(post_id=post)
        self.assertListEqual(
            sorted(tag.tag_name.tag_name for tag in tags),
            sorted(["tag1", "tag2"]),
        )

    def test_create_post_post_request_invalid_data(self):
        """Test that an invalid POST request does not create a post."""
        response = self.client.post(self.url, self.invalid_data, follow=True)

        # Assert that no post is created
        self.assertEqual(Post.objects.count(), 0)

        # Assert that validation errors are displayed
        form_errors = response.context["post_form"].errors
        self.assertIn("image", form_errors)  # Image is required
        self.assertEqual(form_errors["image"][0], "No file selected!")  

    def test_create_post_unauthenticated(self):
        """Test that an unauthenticated user is redirected to login."""
        self.client.logout()
        response = self.client.get(self.url)

        # Assert redirect to login
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")


class TagSuggestionsViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("tag_suggestions")

        # Create sample tags
        self.tag1 = ImageTags.objects.create(tag_name="nature")
        self.tag2 = ImageTags.objects.create(tag_name="technology")
        self.tag3 = ImageTags.objects.create(tag_name="travel")
        self.tag4 = ImageTags.objects.create(tag_name="health")

    def test_tag_suggestions_with_query(self):
        """
        Test that the view returns tags that match the query.
        """
        response = self.client.get(self.url, {"q": "tech"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        # Parse the response data
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)  # Only "technology" matches
        self.assertEqual(data[0]["tag_name"], "technology")

    def test_tag_suggestions_with_partial_query(self):
        """
        Test that the view returns tags that partially match the query.
        """
        response = self.client.get(self.url, {"q": "t"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        # Parse the response data
        data = json.loads(response.content)
        self.assertGreaterEqual(len(data), 2)  # "technology" and "travel" match
        tag_names = [tag["tag_name"] for tag in data]
        self.assertIn("technology", tag_names)
        self.assertIn("travel", tag_names)

    def test_tag_suggestions_with_no_query(self):
        """
        Test that the view returns the first 10 tags when no query is provided.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        # Parse the response data
        data = json.loads(response.content)
        self.assertEqual(len(data), min(10, ImageTags.objects.count()))
        tag_names = [tag["tag_name"] for tag in data]
        self.assertIn("nature", tag_names)
        self.assertIn("technology", tag_names)
        self.assertIn("travel", tag_names)
        self.assertIn("health", tag_names)

    def test_tag_suggestions_with_no_results(self):
        """
        Test that the view returns an empty list when no tags match the query.
        """
        response = self.client.get(self.url, {"q": "nonexistent"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        # Parse the response data
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)


class AddCommentViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create a test post
        self.post = Post.objects.create(
            image='test_image.jpg',
            title='Test Post',
            user=self.user,
            description='This is a test post',
            likes=0,
            created_on=now()
        )

        # Define the URL for adding a comment
        self.url = reverse('add_comment', kwargs={'post_id': str(self.post.id)})

    def test_add_comment_valid_data(self):
        """
        Test that a valid AJAX POST request adds a comment to the post.
        """
        self.client.login(username='testuser', password='testpass')

        data = {'body': 'This is a test comment.'}
        headers = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        response = self.client.post(self.url, data, **headers)

        # Check the response status
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['body'], 'This is a test comment.')
        self.assertEqual(response_data['author'], self.user.username)
        self.assertIn('created_on', response_data)

        # Ensure the comment was saved in the database
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.body, 'This is a test comment.')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.post, self.post)

    def test_add_comment_invalid_data(self):
        """
        Test that an AJAX POST request with invalid data does not add a comment.
        """
        self.client.login(username='testuser', password='testpass')

        # Send empty data
        data = {'body': ''}
        headers = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        response = self.client.post(self.url, data, **headers)

        # Check the response status
        self.assertEqual(response.status_code, 400)

        # Parse the JSON response
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Invalid form data')

        # Ensure no comment was created
        self.assertEqual(Comment.objects.count(), 0)

    def test_add_comment_non_ajax_request(self):
        """
        Test that a non-AJAX request returns an error.
        """
        self.client.login(username='testuser', password='testpass')

        data = {'body': 'This is a test comment.'}

        response = self.client.post(self.url, data)

        # Check the response status
        self.assertEqual(response.status_code, 400)

        # Parse the JSON response
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Invalid request')

        # Ensure no comment was created
        self.assertEqual(Comment.objects.count(), 0)

    def test_add_comment_unauthenticated(self):
        """
        Test that an unauthenticated user cannot add a comment.
        """
        data = {'body': 'This is a test comment.'}
        headers = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        response = self.client.post(self.url, data, **headers)

        # Check that the response is a redirect to the login page
        login_url = reverse('account_login')  # Replace with your LOGIN_URL name
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(login_url))

        # Ensure no comment was created
        self.assertEqual(Comment.objects.count(), 0)


class CommentDeleteViewTest(TestCase):

    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.user3 = User.objects.create_user(username="user3", password="password123")

        # Create a post
        self.post = Post.objects.create(
            user=self.user1,
            image="test_image.jpg",
            title="Test Post",
            description="Test Description"
        )

        # Create comments
        self.comment_by_user1 = Comment.objects.create(
            post=self.post,
            author=self.user1,
            body="Comment by user1"
        )
        self.comment_by_user2 = Comment.objects.create(
            post=self.post,
            author=self.user2,
            body="Comment by user2"
        )

    def test_comment_delete_own_comment(self):
        """Test that a user can delete their own comment."""
        self.client.login(username="user1", password="password123")
        url = reverse('delete_comment', args=[self.post.id, self.comment_by_user1.id])
        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('post_detail', args=[self.post.id]))
        self.assertEqual(Comment.objects.filter(id=self.comment_by_user1.id).count(), 0)

        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Comment deleted!", [message.message for message in messages])

    def test_post_user_can_delete_comment(self):
        """Test that the post's author can delete any comment on their post."""
        self.client.login(username="user1", password="password123")
        url = reverse('delete_comment', args=[self.post.id, self.comment_by_user2.id])
        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('post_detail', args=[self.post.id]))
        self.assertEqual(Comment.objects.filter(id=self.comment_by_user2.id).count(), 0)

        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Comment deleted!", [message.message for message in messages])


class UpdateCommentViewTest(TestCase):

    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        # Create a post
        self.post = Post.objects.create(
            user=self.user1,
            image="test_image.jpg",
            title="Test Post",
            description="Test Description"
        )

        # Create a comment
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user1,
            body="Original Comment"
        )

        self.url = reverse('edit_comment', args=[self.post.id, self.comment.id])

    def test_update_comment_success(self):
        """Test that a user can successfully update their own comment."""
        self.client.login(username="user1", password="password123")
        response = self.client.post(
            self.url,
            data=json.dumps({'body': 'Updated Comment'}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('success'), True)
        self.assertEqual(response.json().get('body'), 'Updated Comment')

        # Check the comment was updated in the database
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.body, 'Updated Comment')

    def test_update_comment_invalid_method(self):
        """Test that a non-POST request returns a 405 error."""
        self.client.login(username="user1", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json().get('error'), 'Invalid request method.')

    def test_update_comment_unauthorized_user(self):
        """Test that a user cannot edit another user's comment."""
        self.client.login(username="user2", password="password123")
        response = self.client.post(
            self.url,
            data=json.dumps({'body': 'Updated Comment'}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json().get('error'), 'You are not authorized to edit this comment.')

    def test_update_comment_empty_body(self):
        """Test that an empty comment body returns a 400 error."""
        self.client.login(username="user1", password="password123")
        response = self.client.post(
            self.url,
            data=json.dumps({'body': ''}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), 'Comment body cannot be empty.')

    def test_update_comment_invalid_json(self):
        """Test that invalid JSON data returns a 400 error."""
        self.client.login(username="user1", password="password123")
        response = self.client.post(
            self.url,
            data="Invalid JSON String",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), 'Invalid JSON data.')

    def test_update_comment_unauthenticated(self):
        """Test that an unauthenticated user cannot update a comment."""
        response = self.client.post(
            self.url,
            data=json.dumps({'body': 'Updated Comment'}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn(reverse('account_login'), response.url)


class PostDeleteViewTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="user", password="password123")
        self.other_user = User.objects.create_user(username="other_user", password="password123")

        # Create a post
        self.post = Post.objects.create(
            user=self.user,
            image="test_image.jpg",
            title="Test Post",
            description="Test Description"
        )

        self.url = reverse('post_delete', args=[self.post.id])

    def test_post_delete_success(self):
        """Test that a user can successfully delete their own post."""
        self.client.login(username="user", password="password123")
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('home'))

        # Check that the post has been deleted
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_post_delete_unauthorized_user(self):
        """Test that a user cannot delete a post they do not own."""
        self.client.login(username="other_user", password="password123")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

        # Check that the post still exists
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())

    def test_post_delete_unauthenticated_user(self):
        """Test that an unauthenticated user cannot delete a post."""
        response = self.client.post(self.url)
        self.assertRedirects(response, f"{reverse('account_login')}?next={self.url}")

        # Check that the post still exists
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())

    def test_post_delete_invalid_method(self):
        """Test that a non-POST request does not delete the post."""
        self.client.login(username="user", password="password123")
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('post_detail', args=[self.post.id]))

        # Check that the post still exists
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())