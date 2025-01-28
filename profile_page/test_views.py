from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from profile_page.models import Profile, ImageBoard, BoardImageRelationship
from post.models import Post


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