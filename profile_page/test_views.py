from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from profile_page.models import Profile, ImageBoard, BoardImageRelationship
from post.models import Post
from django.core.paginator import Page


class ProfilePageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users
        cls.user = User.objects.create_user(username="testuser", password="password123")
        cls.other_user = User.objects.create_user(username="otheruser", password="password456")

        # Create the profile explicitly
        cls.profile, _ = Profile.objects.get_or_create(user=cls.user)

        # Create "All Pins" board explicitly (Public)
        cls.all_pins_board, _ = ImageBoard.objects.get_or_create(
            user=cls.user,
            title="All Pins",
            visibility=0,  # Public
        )

        # Create a private board
        cls.private_board = ImageBoard.objects.create(
            user=cls.user,
            title="Private Board",
            visibility=1,  # Private
        )

        cls.profile_url = reverse("profile_page", kwargs={"username": cls.user.username})

    def test_profile_page_renders_correct_template(self):
        """Test that the profile page renders the correct template."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile_page/profile_page.html")

    def test_profile_creation(self):
        """Test that a profile is created automatically if it does not exist."""
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user, self.user)

    def test_all_pins_board_creation(self):
        """Test that the 'All Pins' board is created automatically for the user."""
        all_pins_board = ImageBoard.objects.filter(user=self.user, title="All Pins").first()
        self.assertIsNotNone(all_pins_board)
        self.assertEqual(all_pins_board.visibility, 0)  # Public

    def test_redirect_to_lowercase_username(self):
        """Test that the profile page redirects to a lowercase username if accessed with a different case."""
        uppercase_url = reverse("profile_page", kwargs={"username": self.user.username.upper()})
        response = self.client.get(uppercase_url)
        self.assertRedirects(response, self.profile_url)


    def test_posts_pinned_to_all_pins_board(self):
        """Test that posts saved to other boards are automatically pinned to the 'All Pins' board."""
        # Create test posts associated with the user
        post1 = Post.objects.create(title="Post 1", user=self.user, description="Test post 1")
        post2 = Post.objects.create(title="Post 2", user=self.user, description="Test post 2")

        # Pin posts to the private board
        BoardImageRelationship.objects.create(post_id=post1, board_id=self.private_board)
        BoardImageRelationship.objects.create(post_id=post2, board_id=self.private_board)

        # Fetch posts pinned to "All Pins"
        all_pins_posts = Post.objects.filter(
            pinned_image__board_id=self.all_pins_board
        ).distinct()

        # Assert posts are in the "All Pins" board
        self.assertIn(post1, all_pins_posts)
        self.assertIn(post2, all_pins_posts)
        self.assertEqual(all_pins_posts.count(), 2)

    def test_profile_page_shows_correct_user_info(self):
        """Test that the profile page shows the correct user information."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.profile.first_name or "")
        self.assertContains(response, self.profile.last_name or "")

    def test_authenticated_other_user_access(self):
        """Test that an authenticated user can access another user's profile page."""
        self.client.login(username="otheruser", password="password456")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    
class CreatedPinsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password123")
        cls.other_user = User.objects.create_user(username="otheruser", password="password456")

        for i in range(25):
            Post.objects.create(title=f"Post {i + 1}", description=f"Description {i + 1}", user=cls.user)

        cls.created_pins_url = reverse("created_pins", kwargs={"username": cls.user.username})

    def test_view_url_exists_at_desired_location(self):
        """Test that the view returns a 200 status code."""
        response = self.client.get(self.created_pins_url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test that the correct template is used."""
        response = self.client.get(self.created_pins_url)
        self.assertTemplateUsed(response, "profile_page/created_pins.html")

    def test_view_renders_user_posts(self):
        """Test that the created posts are displayed for the user."""
        response = self.client.get(self.created_pins_url)

        # Check if the first page of posts is displayed
        for i in range(25, 15, -1):  # Posts 25 to 16
            self.assertContains(response, f"Post {i}")

    def test_pagination_renders_correctly(self):
        """Test that the pagination shows the correct number of posts per page."""
        response = self.client.get(self.created_pins_url)
        self.assertEqual(len(response.context['created_posts']), 10)

    def test_pagination_second_page(self):
        """Test that the second page contains the correct posts."""
        response = self.client.get(self.created_pins_url + "?page=2")

        # Check if the second page renders posts 15 to 6
        for i in range(15, 5, -1):
            self.assertContains(response, f"Post {i}")
        self.assertNotContains(response, "Post 25")  # Ensure first-page content is not shown

    def test_pagination_empty_page(self):
        """Test that an empty page returns an empty response."""
        response = self.client.get(self.created_pins_url + "?page=999")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode().strip(), "")  # Expect empty response for out-of-range pages

    def test_view_for_case_insensitive_username(self):
        """Test that the view works with a case-insensitive username."""
        url_with_uppercase_username = reverse("created_pins", kwargs={"username": self.user.username.upper()})
        response = self.client.get(url_with_uppercase_username)

        # Check if the first page of posts is displayed
        for i in range(25, 15, -1):  # Posts 25 to 16
            self.assertContains(response, f"Post {i}")

    def test_view_no_posts(self):
        """Test that the view handles users with no posts gracefully."""
        no_posts_url = reverse("created_pins", kwargs={"username": self.other_user.username})
        response = self.client.get(no_posts_url)

        # Ensure no posts are rendered
        self.assertNotContains(response, '<div class="grid-item">')

    def test_next_page_link_renders_correctly(self):
        """Test that the next page link is rendered for paginated content."""
        response = self.client.get(self.created_pins_url)

        # Check if the link for the next page is rendered
        self.assertContains(response, f'?page=2')
