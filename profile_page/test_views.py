from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from profile_page.models import Profile, ImageBoard, BoardImageRelationship
from post.models import Post
from django.core.paginator import Page
from django.db.models import Count


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


class ImageBoardsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users
        cls.user = User.objects.create_user(username="testuser", password="password123")
        cls.other_user = User.objects.create_user(username="otheruser", password="password456")
        
        # Create a profile for the users
        Profile.objects.create(user=cls.user)
        Profile.objects.create(user=cls.other_user)

        # Create "All Pins" board and other boards for the user
        cls.all_pins_board = ImageBoard.objects.create(user=cls.user, title="All Pins", visibility=0)
        cls.board1 = ImageBoard.objects.create(user=cls.user, title="Board 1", visibility=0)
        cls.board2 = ImageBoard.objects.create(user=cls.user, title="Board 2", visibility=0)

        # Create posts and associate them with boards
        for i in range(5):
            post = Post.objects.create(title=f"Post {i + 1}", description=f"Description {i + 1}", user=cls.user)
            BoardImageRelationship.objects.create(post_id=post, board_id=cls.board1)

        for i in range(3):
            post = Post.objects.create(title=f"Post {i + 6}", description=f"Description {i + 6}", user=cls.user)
            BoardImageRelationship.objects.create(post_id=post, board_id=cls.board2)

        for i in range(2):
            post = Post.objects.create(title=f"Post {i + 9}", description=f"Description {i + 9}", user=cls.user)
            BoardImageRelationship.objects.create(post_id=post, board_id=cls.all_pins_board)

        cls.image_boards_url = reverse("image_boards", kwargs={"username": cls.user.username})

    def test_view_uses_correct_template(self):
        """Test that the correct template is used."""
        response = self.client.get(self.image_boards_url)
        self.assertTemplateUsed(response, "profile_page/image_boards.html")

    def test_view_displays_boards_with_images(self):
        """Test that boards and their associated images are displayed."""
        response = self.client.get(self.image_boards_url)
        
        # Check "All Pins" board displays up to 3 images
        self.assertContains(response, "All Pins")
        self.assertContains(response, "Post 1")
        self.assertContains(response, "Post 2")
        self.assertContains(response, "Post 3")
        self.assertNotContains(response, "Post 4")  # Should not show more than 3 images

        # Check "Board 1" and its associated posts
        self.assertContains(response, "Board 1")
        self.assertContains(response, "Post 1")
        self.assertContains(response, "Post 2")
        self.assertContains(response, "Post 3")
        self.assertNotContains(response, "Post 4")  # Only 3 images per board

        # Check "Board 2" and its associated posts
        self.assertContains(response, "Board 2")
        self.assertContains(response, "Post 6")
        self.assertContains(response, "Post 7")
        self.assertContains(response, "Post 8")
        self.assertNotContains(response, "Post 9")  # Should not show more than 3 images

    def test_view_handles_no_boards(self):
        """Test that the view handles users with no boards gracefully."""
        # Create a new user with no boards except the default "All Pins"
        no_boards_user = User.objects.create_user(username="noboardsuser", password="password123")
        Profile.objects.create(user=no_boards_user)

        no_boards_url = reverse("image_boards", kwargs={"username": no_boards_user.username})
        response = self.client.get(no_boards_url)

        # Ensure that only the "All Pins" board is displayed and it's empty
        self.assertContains(response, "All Pins")
        self.assertContains(response, '<div class="tile-image large"></div>', count=1)
        self.assertContains(response, '<div class="tile-image small"></div>', count=2)
        self.assertNotContains(response, "Board 1")  # No additional boards should be rendered

    def test_view_displays_no_images_when_board_is_empty(self):
        """Test that the view displays boards even if they have no associated images."""
        BoardImageRelationship.objects.filter(board_id=self.board1).delete()
        response = self.client.get(self.image_boards_url)

        # Ensure the empty board is still displayed
        self.assertContains(response, "Board 1")
        # Check that the placeholders for images are rendered
        self.assertContains(response, '<div class="tile-image large"></div>', count=1)
        self.assertContains(response, '<div class="tile-image small"></div>', count=2)

    def test_view_displays_private_all_pins_to_owner(self):
        """Test that the 'All Pins' board is displayed to the owner even if it's private."""
        self.all_pins_board.visibility = 1  # Make it private
        self.all_pins_board.save()

        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.image_boards_url)

        self.assertContains(response, "All Pins")
        self.assertContains(response, "Post 1")

    def test_view_hides_private_all_pins_from_other_user(self):
        """Test that the 'All Pins' board is hidden from other users if it's private."""
        self.all_pins_board.visibility = 1  # Make it private
        self.all_pins_board.save()

        self.client.login(username="otheruser", password="password456")
        response = self.client.get(self.image_boards_url)

        self.assertNotContains(response, "All Pins")

    def test_view_displays_public_boards_to_other_user(self):
        """Test that public boards are displayed to other users."""
        self.board1.visibility = 0  # Public
        self.board1.save()

        self.client.login(username="otheruser", password="password456")
        response = self.client.get(self.image_boards_url)

        self.assertContains(response, "Board 1")
        self.assertContains(response, "Post 1")

    def test_view_does_not_display_private_boards_to_other_user(self):
        """Test that private boards are not displayed to other users."""
        self.board2.visibility = 1  # Make it private
        self.board2.save()

        self.client.login(username="otheruser", password="password456")
        response = self.client.get(self.image_boards_url)

        self.assertNotContains(response, "Board 2")

    def test_view_redirects_for_invalid_user(self):
        """Test that the view returns a 404 for a non-existent user."""
        response = self.client.get(reverse("image_boards", kwargs={"username": "nonexistentuser"}))
        self.assertEqual(response.status_code, 404)

    def test_view_pagination_of_boards(self):
        """Test that the view handles pagination correctly when there are many boards."""
        # Create additional boards to test pagination
        for i in range(10):
            ImageBoard.objects.create(user=self.user, title=f"Extra Board {i + 1}", visibility=0)

        response = self.client.get(self.image_boards_url)
        self.assertContains(response, "Board 1")
        self.assertContains(response, "Extra Board 10")
        self.assertNotContains(response, "Extra Board 11")  # Should not display more than the allowed number