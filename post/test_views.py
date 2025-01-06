from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from uuid import uuid4
from post.models import Post, Comment
from profile_page.models import ImageBoard


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