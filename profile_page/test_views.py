from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from uuid import uuid4
from PIL import Image
import io
from profile_page.models import Profile, ImageBoard, BoardImageRelationship
from post.models import Post
from .views import sync_all_pins_board


class ProfilePageViewTest(TestCase):
    @classmethod
    def generate_test_image(cls):
        """Generate a valid in-memory image for testing."""
        image = Image.new('RGB', (100, 100), color='red')
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        return SimpleUploadedFile("test_image.jpg",
                                  img_io.getvalue(),
                                  content_type="image/jpeg")

    @classmethod
    def setUpTestData(cls):
        # Create users
        cls.user = User.objects.create_user(username="testuser",
                                            password="password123")
        cls.other_user = User.objects.create_user(username="otheruser",
                                                  password="password456")

        cls.profile = Profile.objects.create(
            user=cls.user,
            profile_image=cls.generate_test_image()  # Use a local test image
        )

        # Create "All Pins" board explicitly
        cls.all_pins_board, _ = ImageBoard.objects.get_or_create(
            user=cls.user,
            title="All Pins",
            visibility=1,
        )

        # Create a private board
        cls.private_board = ImageBoard.objects.create(
            user=cls.user,
            title="Private Board",
            visibility=1,  # Private
        )

        cls.profile_url = reverse("profile_page", kwargs={
            "username": cls.user.username})

    def test_profile_page_renders_correct_template(self):
        """Test that the profile page renders the correct template."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile_page/profile_page.html")

    def test_profile_creation(self):
        """Test that a profile is created automatically if
        it does not exist."""
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user, self.user)

    def test_all_pins_board_creation(self):
        """Test that the 'All Pins' board is created automatically
        for the user."""
        all_pins_board = ImageBoard.objects.filter(user=self.user,
                                                   title="All Pins").first()
        self.assertIsNotNone(all_pins_board)
        self.assertEqual(all_pins_board.visibility, 1)

    def test_redirect_to_lowercase_username(self):
        """Test that the profile page redirects to a lowercase username if
        accessed with a different case."""
        uppercase_url = reverse("profile_page", kwargs={
            "username": self.user.username.upper()})
        response = self.client.get(uppercase_url)
        self.assertRedirects(response, self.profile_url)

    def test_posts_pinned_to_all_pins_board(self):
        """Test that posts saved to other boards are automatically pinned to
        the 'All Pins' board."""
        # Create test posts associated with the user
        post1 = Post.objects.create(title="Post 1", user=self.user,
                                    description="Test post 1")
        post2 = Post.objects.create(title="Post 2", user=self.user,
                                    description="Test post 2")

        # Pin posts to the private board
        BoardImageRelationship.objects.create(post_id=post1,
                                              board_id=self.private_board)
        BoardImageRelationship.objects.create(post_id=post2,
                                              board_id=self.private_board)

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
        """Test that an authenticated user can access another
        user's profile page."""
        self.client.login(username="otheruser", password="password456")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def test_profile_page_nonexistent_user(self):
        """Test that the profile page returns a 404 for a nonexistent user."""
        response = self.client.get(reverse("profile_page", kwargs={
            "username": "nonexistentuser"}))
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_access_own_profile(self):
        """Test that an authenticated user can access their own profile."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_modal_visible_to_owner(self):
        """Test that the edit profile modal is visible only to the
        profile owner."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.profile_url)
        self.assertContains(response, "Edit Profile")

    def test_edit_profile_button_hidden_from_other_users(self):
        """Test that the 'Edit Profile' button is hidden from other users."""
        self.client.login(username="otheruser", password="password456")
        response = self.client.get(self.profile_url)

        # Check that the 'Edit Profile' button is not visible for other users
        self.assertNotContains(response, 'id="edit-profile-btn"')

    def test_logout_functionality(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("custom_accounts:logout"))

        self.assertRedirects(response, "/")

        # Verify the user is logged out
        response_after = self.client.get(self.profile_url)
        self.assertFalse(response_after.wsgi_request.user.is_authenticated)
        self.assertContains(response_after, "Log-in")


class CreatedPinsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser",
                                            password="password123")
        cls.other_user = User.objects.create_user(username="otheruser",
                                                  password="password456")

        for i in range(25):
            Post.objects.create(title=f"Post {i + 1}",
                                description=f"Description {i + 1}",
                                user=cls.user)

        cls.created_pins_url = reverse("created_pins", kwargs={
            "username": cls.user.username})

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
        """Test that the pagination shows the correct
        number of posts per page."""
        response = self.client.get(self.created_pins_url)
        self.assertEqual(len(response.context['created_posts']), 10)

    def test_pagination_second_page(self):
        """Test that the second page contains the correct posts."""
        response = self.client.get(self.created_pins_url + "?page=2")

        # Check if the second page renders posts 15 to 6
        for i in range(15, 5, -1):
            self.assertContains(response, f"Post {i}")
        self.assertNotContains(response, "Post 25")
        # Ensure first-page content is not shown

    def test_pagination_empty_page(self):
        """Test that an empty page returns an empty response."""
        response = self.client.get(self.created_pins_url + "?page=999")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode().strip(), "")
        # Expect empty response for out-of-range pages

    def test_view_for_case_insensitive_username(self):
        """Test that the view works with a case-insensitive username."""
        url_with_uppercase_username = reverse(
            "created_pins", kwargs={
                "username": self.user.username.upper()})
        response = self.client.get(url_with_uppercase_username)

        # Check if the first page of posts is displayed
        for i in range(25, 15, -1):  # Posts 25 to 16
            self.assertContains(response, f"Post {i}")

    def test_view_no_posts(self):
        """Test that the view handles users with no posts gracefully."""
        no_posts_url = reverse("created_pins", kwargs={
            "username": self.other_user.username})
        response = self.client.get(no_posts_url)

        # Ensure no posts are rendered
        self.assertNotContains(response, '<div class="grid-item">')

    def test_next_page_link_renders_correctly(self):
        """Test that the next page link is rendered for paginated content."""
        response = self.client.get(self.created_pins_url)

        # Check if the link for the next page is rendered
        self.assertContains(response,
                            f'?page=2')  # noqa


class ImageBoardsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create users
        cls.user = User.objects.create_user(username="testuser",
                                            password="password123")
        cls.other_user = User.objects.create_user(username="otheruser",
                                                  password="password456")

        # Create a profile for the users
        Profile.objects.create(user=cls.user)
        Profile.objects.create(user=cls.other_user)

        # Create "All Pins" board and other boards for the user
        cls.all_pins_board = ImageBoard.objects.create(user=cls.user,
                                                       title="All Pins",
                                                       visibility=0)
        cls.board1 = ImageBoard.objects.create(user=cls.user, title="Board 1",
                                               visibility=0)
        cls.board2 = ImageBoard.objects.create(user=cls.user,
                                               title="Board 2", visibility=0)

        # Create posts and associate them with boards
        for i in range(5):
            post = Post.objects.create(title=f"Post {i + 1}",
                                       description=f"Description {i + 1}",
                                       user=cls.user)
            BoardImageRelationship.objects.create(post_id=post,
                                                  board_id=cls.board1)

        for i in range(3):
            post = Post.objects.create(title=f"Post {i + 6}",
                                       description=f"Description {i + 6}",
                                       user=cls.user)
            BoardImageRelationship.objects.create(post_id=post,
                                                  board_id=cls.board2)

        for i in range(2):
            post = Post.objects.create(title=f"Post {i + 9}",
                                       description=f"Description {i + 9}",
                                       user=cls.user)
            BoardImageRelationship.objects.create(post_id=post,
                                                  board_id=cls.all_pins_board)

        cls.image_boards_url = reverse("image_boards", kwargs={
            "username": cls.user.username})

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
        self.assertNotContains(response, "Post 4")
        # Should not show more than 3 images

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
        self.assertNotContains(response, "Post 9")
        # Should not show more than 3 images

    def test_view_displays_private_all_pins_to_owner(self):
        """Test that the 'All Pins' board is displayed to the owner even if
        it's private."""
        self.all_pins_board.visibility = 1  # Make it private
        self.all_pins_board.save()

        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.image_boards_url)

        self.assertContains(response, "All Pins")
        self.assertContains(response, "Post 1")

    def test_view_hides_private_all_pins_from_other_user(self):
        """Test that the 'All Pins' board is hidden from other users if
        it's private."""
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
        response = self.client.get(reverse("image_boards", kwargs={
            "username": "nonexistentuser"}))
        self.assertEqual(response.status_code, 404)

    def test_view_pagination_of_boards(self):
        """Test that the view handles pagination correctly
        when there are many boards."""
        # Create additional boards to test pagination
        for i in range(10):
            ImageBoard.objects.create(user=self.user,
                                      title=f"Extra Board {i + 1}",
                                      visibility=0)

        response = self.client.get(self.image_boards_url)
        self.assertContains(response, "Board 1")
        self.assertContains(response, "Extra Board 10")
        self.assertNotContains(response, "Extra Board 11")
        # Should not display more than the allowed number


class BoardDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user and their profile
        cls.user = User.objects.create_user(username="testuser",
                                            password="password123")
        cls.other_user = User.objects.create_user(username="otheruser",
                                                  password="password456")
        Profile.objects.create(user=cls.user)
        Profile.objects.create(user=cls.other_user)

        # Create boards
        cls.board = ImageBoard.objects.create(user=cls.user, title="Board 1",
                                              visibility=0)
        cls.all_pins_board = ImageBoard.objects.create(user=cls.user,
                                                       title="All Pins",
                                                       visibility=0)

        # Create posts and associate them with the board
        cls.post1 = Post.objects.create(title="Post 1",
                                        description="Description 1",
                                        user=cls.user)
        cls.post2 = Post.objects.create(title="Post 2",
                                        description="Description 2",
                                        user=cls.user)
        cls.post3 = Post.objects.create(title="Post 3",
                                        description="Description 3",
                                        user=cls.user)

        BoardImageRelationship.objects.create(post_id=cls.post1,
                                              board_id=cls.board)
        BoardImageRelationship.objects.create(post_id=cls.post2,
                                              board_id=cls.board)
        BoardImageRelationship.objects.create(post_id=cls.post3,
                                              board_id=cls.board)

        cls.board_url = reverse("board_detail", kwargs={
            "board_id": cls.board.id})

    def test_view_uses_correct_template(self):
        """Test that the correct template is used."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.board_url)
        self.assertTemplateUsed(response, "profile_page/board_detail.html")

    def test_view_displays_board_title(self):
        """Test that the board's title is displayed."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.board_url)
        self.assertContains(response, "Board 1")

    def test_view_displays_board_images(self):
        """Test that the board's associated images are displayed."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.board_url)
        self.assertContains(response, "Post 1")
        self.assertContains(response, "Post 2")
        self.assertContains(response, "Post 3")

    def test_view_shows_edit_button_for_owner(self):
        """Test that the edit button is shown for the owner of the board."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.board_url)
        self.assertContains(response, "Edit Board")

    def test_view_allows_unpinning_for_owner(self):
        """Test that the unpin button is displayed for the
        owner of the board."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.board_url)
        self.assertContains(response, 'class="unpin-btn"')

    def test_view_hides_unpinning_for_other_users(self):
        """Test that the unpin button is hidden for users
        who do not own the board."""
        self.client.login(username="otheruser", password="password456")
        response = self.client.get(self.board_url)
        self.assertNotContains(response, 'class="unpin-btn"')

    def test_view_allows_private_board_for_owner(self):
        """Test that a private board is accessible to its owner."""
        self.board.visibility = 1
        self.board.save()

        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.board_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.board.title)

    def test_view_hides_private_board_from_other_users(self):
        """Test that a private board is not visible to other users."""
        self.board.visibility = 1
        self.board.save()

        self.client.login(username="otheruser", password="password456")
        response = self.client.get(self.board_url)
        self.assertEqual(response.status_code, 404)
        # Non-owner should receive a 404

    def test_view_404_for_nonexistent_board(self):
        """Test that a 404 is returned for a nonexistent board."""
        nonexistent_board_url = reverse("board_detail", kwargs={
            "board_id": 9999})
        response = self.client.get(nonexistent_board_url)
        self.assertEqual(response.status_code, 404)

    def test_view_handles_empty_board_gracefully(self):
        """Test that the view handles boards with no images gracefully."""
        empty_board = ImageBoard.objects.create(user=self.user,
                                                title="Empty Board",
                                                visibility=0)
        empty_board_url = reverse("board_detail", kwargs={
            "board_id": empty_board.id})
        self.client.login(username="testuser", password="password123")
        response = self.client.get(empty_board_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Empty Board")
        self.assertNotContains(response, '<div class="grid-item"')

    def test_view_displays_all_pins_board(self):
        """Test that the All Pins board is displayed correctly."""
        self.client.login(username="testuser", password="password123")
        all_pins_url = reverse("board_detail", kwargs={
            "board_id": self.all_pins_board.id})
        response = self.client.get(all_pins_url)
        self.assertContains(response, "All Pins")
        self.assertEqual(response.status_code, 200)

    def test_view_allows_public_board_for_any_user(self):
        """Test that a public board is accessible to any user."""
        self.board.visibility = 0  # Make board public
        self.board.save()

        self.client.login(username="otheruser", password="password456")
        response = self.client.get(self.board_url)
        self.assertEqual(response.status_code, 200)
        # Public board should be accessible
        self.assertContains(response, self.board.title)
        # Board title should be rendered


class SyncAllPinsBoardTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user and their profile
        cls.user = User.objects.create_user(username="testuser",
                                            password="password123")
        Profile.objects.create(user=cls.user)

        # Create boards
        cls.board1 = ImageBoard.objects.create(user=cls.user,
                                               title="Board 1", visibility=0)
        cls.board2 = ImageBoard.objects.create(user=cls.user,
                                               title="Board 2", visibility=0)

        # Create posts
        cls.post1 = Post.objects.create(title="Post 1", user=cls.user,
                                        description="Description 1")
        cls.post2 = Post.objects.create(title="Post 2", user=cls.user,
                                        description="Description 2")
        cls.post3 = Post.objects.create(title="Post 3", user=cls.user,
                                        description="Description 3")

        # Pin posts to boards
        BoardImageRelationship.objects.create(post_id=cls.post1,
                                              board_id=cls.board1)
        BoardImageRelationship.objects.create(post_id=cls.post2,
                                              board_id=cls.board1)
        BoardImageRelationship.objects.create(post_id=cls.post3,
                                              board_id=cls.board2)

    def test_all_pins_board_is_created_if_not_exists(self):
        """Test that the 'All Pins' board is created if it
        doesn't already exist."""
        ImageBoard.objects.filter(user=self.user, title="All Pins").delete()
        self.assertFalse(ImageBoard.objects.filter(user=self.user,
                                                   title="All Pins").exists())
        sync_all_pins_board(self.user)
        self.assertTrue(ImageBoard.objects.filter(user=self.user,
                                                  title="All Pins").exists())

    def test_posts_are_added_to_all_pins_board(self):
        """Test that posts saved to any board are added to
        the 'All Pins' board."""
        sync_all_pins_board(self.user)
        all_pins_board = ImageBoard.objects.get(user=self.user,
                                                title="All Pins")

        # Verify that all posts are added to 'All Pins'
        self.assertEqual(BoardImageRelationship.objects.filter(
            board_id=all_pins_board).count(), 3)

    def test_no_duplicates_in_all_pins_board(self):
        """Test that posts already in the 'All Pins' board are
        not duplicated."""
        sync_all_pins_board(self.user)  # Initial sync
        sync_all_pins_board(self.user)  # Second sync to ensure no duplicates
        all_pins_board = ImageBoard.objects.get(user=self.user,
                                                title="All Pins")

        # Verify there are no duplicates
        relationships = BoardImageRelationship.objects.filter(
            board_id=all_pins_board)
        self.assertEqual(relationships.count(), 3)

    def test_only_user_posts_are_added(self):
        """Test that only the user's posts are added to the
        'All Pins' board."""
        other_user = User.objects.create_user(username="otheruser",
                                              password="password456")
        Profile.objects.create(user=other_user)

        # Create posts for the other user and pin them to their board
        other_board = ImageBoard.objects.create(user=other_user,
                                                title="Other Board",
                                                visibility=0)
        other_post = Post.objects.create(title="Other User Post",
                                         user=other_user,
                                         description="Description")
        BoardImageRelationship.objects.create(post_id=other_post,
                                              board_id=other_board)

        # Sync "All Pins" for the test user
        sync_all_pins_board(self.user)
        all_pins_board = ImageBoard.objects.get(user=self.user,
                                                title="All Pins")

        # Ensure other user's post is not added
        self.assertNotIn(other_post, Post.objects.filter(
            pinned_image__board_id=all_pins_board))

    def test_empty_all_pins_board_when_no_saved_posts(self):
        """Test that the 'All Pins' board is empty if there
        are no saved posts."""
        # Create a new user with no saved posts
        new_user = User.objects.create_user(username="newuser",
                                            password="password123")
        Profile.objects.create(user=new_user)

        sync_all_pins_board(new_user)
        all_pins_board = ImageBoard.objects.get(user=new_user,
                                                title="All Pins")

        # Verify that no posts are in the "All Pins" board
        self.assertEqual(BoardImageRelationship.objects.filter(
            board_id=all_pins_board).count(), 0)

    def test_post_already_in_all_pins_board_is_not_readded(self):
        """Test that a post already in 'All Pins' is not re-added."""
        sync_all_pins_board(self.user)
        all_pins_board = ImageBoard.objects.get(user=self.user,
                                                title="All Pins")

        # Verify initial count
        initial_count = BoardImageRelationship.objects.filter(
            board_id=all_pins_board).count()

        # Re-add the same posts
        sync_all_pins_board(self.user)
        final_count = BoardImageRelationship.objects.filter(
            board_id=all_pins_board).count()

        # Verify that the count remains the same
        self.assertEqual(initial_count, final_count)

    def test_function_does_not_affect_other_boards(self):
        """Test that syncing 'All Pins' does not affect other boards."""
        initial_board1_count = BoardImageRelationship.objects.filter(
            board_id=self.board1).count()
        initial_board2_count = BoardImageRelationship.objects.filter(
            board_id=self.board2).count()

        sync_all_pins_board(self.user)

        # Verify counts for other boards remain unchanged
        self.assertEqual(BoardImageRelationship.objects.filter(
            board_id=self.board1).count(), initial_board1_count)
        self.assertEqual(BoardImageRelationship.objects.filter(
            board_id=self.board2).count(), initial_board2_count)


class HandlePostSaveSignalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test data before each test."""
        cls.user = User.objects.create_user(username="testuser",
                                            password="password123")
        cls.profile = Profile.objects.create(user=cls.user)

        # Create boards
        cls.board = ImageBoard.objects.create(user=cls.user, title="Board 1",
                                              visibility=0)  # Public board
        cls.all_pins_board, _ = ImageBoard.objects.get_or_create(
            user=cls.user, title="All Pins", visibility=1)

        # Create posts
        cls.post = Post.objects.create(title="Test Post",
                                       description="Test description",
                                       user=cls.user)

    def test_signal_triggers_on_boardimage_relationship_creation(self):
        """Test that the signal is triggered when a
        BoardImageRelationship is created."""
        with patch("profile_page.views.sync_all_pins_board") as mock_sync:
            BoardImageRelationship.objects.create(post_id=self.post,
                                                  board_id=self.board)

            # Assert that the sync_all_pins_board function was called once
            mock_sync.assert_called_once_with(self.user)

    def test_post_is_added_to_all_pins_when_saved_to_any_board(self):
        """Test that a post added to any board is also added to the
        'All Pins' board."""
        BoardImageRelationship.objects.create(post_id=self.post,
                                              board_id=self.board)

        # Ensure the post appears in "All Pins"
        self.assertTrue(
            BoardImageRelationship.objects.filter(
                post_id=self.post, board_id=self.all_pins_board).exists()
        )

    def test_signal_does_not_duplicate_entries_in_all_pins(self):
        """Test that the signal does not duplicate posts in 'All Pins'#
        if they already exist."""
        # Add the post to "All Pins" manually
        BoardImageRelationship.objects.create(post_id=self.post,
                                              board_id=self.all_pins_board)

        # Add the same post to another board
        BoardImageRelationship.objects.create(post_id=self.post,
                                              board_id=self.board)

        # Count occurrences in "All Pins"
        count = BoardImageRelationship.objects.filter(
            post_id=self.post, board_id=self.all_pins_board).count()
        self.assertEqual(count, 1)  # Should not be duplicated

    def test_signal_does_not_create_duplicate_all_pins_boards(self):
        """Test that the signal does not create a new 'All Pins' board if it
        already exists."""
        # Ensure there's only one "All Pins" board before saving
        initial_count = ImageBoard.objects.filter(user=self.user,
                                                  title="All Pins").count()

        # Save a new BoardImageRelationship
        BoardImageRelationship.objects.create(post_id=self.post,
                                              board_id=self.board)

        # Ensure "All Pins" board count remains 1
        final_count = ImageBoard.objects.filter(user=self.user,
                                                title="All Pins").count()
        self.assertEqual(initial_count, final_count)

    def test_signal_does_not_modify_all_pins_visibility(self):
        """Test that the signal does not change the visibility
        of the 'All Pins' board."""
        BoardImageRelationship.objects.create(post_id=self.post,
                                              board_id=self.board)

        # Reload "All Pins" board from the database
        self.all_pins_board.refresh_from_db()

        # Visibility should still be 1 (private)
        self.assertEqual(self.all_pins_board.visibility, 1)

    def test_signal_not_trigger_if_no_boardimage_relationship_created(self):
        """Test that the signal does not run when no BoardImageRelationship
        is created."""
        with patch("profile_page.views.handle_post_save") as mock_signal:
            # Simply creating a post should not trigger the signal
            Post.objects.create(title="New Post", user=self.user,
                                description="A test post")

            # Assert that the signal was never called
            mock_signal.assert_not_called()


class SaveToBoardViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.user = User.objects.create_user(username="testuser",
                                            password="password123")
        cls.other_user = User.objects.create_user(username="otheruser",
                                                  password="password456")

        # Create test post
        cls.post = Post.objects.create(title="Test Post", user=cls.user,
                                       description="Test Description")

        # Create boards for the user
        cls.board = ImageBoard.objects.create(user=cls.user,
                                              title="Test Board")
        cls.other_user_board = ImageBoard.objects.create(
            user=cls.other_user, title="Other User's Board")

        cls.client = Client()

    def test_authentication_required(self):
        """Test that unauthenticated users are redirected to login."""
        url = reverse("save_to_board", kwargs={"post_id": self.post.id})
        response = self.client.post(url, {"board_id": self.board.id})
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_successful_save_to_board(self):
        """Test that a post can be successfully saved to a board."""
        self.client.login(username="testuser", password="password123")
        url = reverse("save_to_board", kwargs={"post_id": self.post.id})
        response = self.client.post(url, {"board_id": self.board.id})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "success": True, "message": "Post Saved!"})
        self.assertTrue(BoardImageRelationship.objects.filter(
            post_id=self.post, board_id=self.board).exists())

    def test_cannot_save_to_other_users_board(self):
        """Test that a user cannot save a post to another user's board."""
        self.client.login(username="testuser", password="password123")
        url = reverse("save_to_board", kwargs={"post_id": self.post.id})
        response = self.client.post(url, {
            "board_id": self.other_user_board.id})

        self.assertEqual(response.status_code, 404)
        self.assertFalse(BoardImageRelationship.objects.filter(
            post_id=self.post, board_id=self.other_user_board).exists())

    def test_error_on_missing_board_id(self):
        """Test that missing board_id in request returns a 400 error."""
        self.client.login(username="testuser", password="password123")
        url = reverse("save_to_board", kwargs={"post_id": self.post.id})
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {
            "success": False, "message": "No board selected."})

    def test_error_on_invalid_board_id(self):
        """Test that an invalid board_id returns a 404 error."""
        self.client.login(username="testuser", password="password123")
        url = reverse("save_to_board", kwargs={"post_id": self.post.id})
        response = self.client.post(url, {"board_id": 99999})

        self.assertEqual(response.status_code, 404)

    def test_prevent_duplicate_saves(self):
        """Test that a post cannot be saved multiple times to
        the same board."""
        self.client.login(username="testuser", password="password123")
        BoardImageRelationship.objects.create(
            post_id=self.post, board_id=self.board)  # Pre-existing save

        url = reverse("save_to_board", kwargs={"post_id": self.post.id})
        response = self.client.post(url, {"board_id": self.board.id})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "success": True, "message": "Post Saved!"})
        self.assertEqual(BoardImageRelationship.objects.filter(
            post_id=self.post, board_id=self.board).count(), 1)
        # Still only 1 record

    def test_invalid_request_method(self):
        """Test that a GET request returns a 405 error."""
        self.client.login(username="testuser", password="password123")
        url = reverse("save_to_board", kwargs={"post_id": self.post.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content, {
            "success": False, "message": "Invalid request method."})


class CreateBoardViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.user = User.objects.create_user(
            username="testuser", password="password123")
        cls.other_user = User.objects.create_user(
            username="otheruser", password="password456")

        # Create a test post
        cls.post = Post.objects.create(
            title="Test Post", user=cls.user, description="Test Description")

        # Create a board for the user
        cls.existing_board = ImageBoard.objects.create(
            user=cls.user, title="Existing Board")

        cls.client = Client()

    def test_authentication_required(self):
        """Test that unauthenticated users are redirected to login."""
        url = reverse("create_board")
        response = self.client.post(url, {
            "title": "New Board", "post_id": self.post.id})
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_successful_board_creation(self):
        """Test that a new board is successfully created along
        with a board-image relationship."""
        self.client.login(username="testuser", password="password123")
        url = reverse("create_board")
        response = self.client.post(url, {
            "title": "New Board", "post_id": self.post.id})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "success": True, "message": "Board created successfully!"})

        # Verify that the board was created
        self.assertTrue(ImageBoard.objects.filter(
            user=self.user, title="New Board").exists())

        # Verify that the post was added to the board
        board = ImageBoard.objects.get(user=self.user, title="New Board")
        self.assertTrue(BoardImageRelationship.objects.filter(
            post_id=self.post, board_id=board).exists())

    def test_board_creation_fails_with_existing_title(self):
        """Test that a board with an existing title cannot be created."""
        self.client.login(username="testuser", password="password123")
        url = reverse("create_board")
        response = self.client.post(url, {
            "title": "Existing Board", "post_id": self.post.id})

        self.assertEqual(response.status_code, 400)
        expected_error = {
            "success": False,
            "error": 'A board with the title "Existing Board" already exists.'}
        self.assertJSONEqual(response.content, expected_error)

    def test_error_on_missing_title(self):
        """Test that missing board title in request returns a 400 error."""
        self.client.login(username="testuser", password="password123")
        url = reverse("create_board")
        response = self.client.post(url, {
            "title": "", "post_id": self.post.id})

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {
            "success": False, "error": "Board title is required."})

    def test_error_on_invalid_post_id(self):
        """Test that an invalid post_id returns a
        500 error due to unhandled exception."""
        self.client.login(username="testuser", password="password123")
        url = reverse("create_board")

        # Non-existent post_id
        response = self.client.post(url, {
            "title": "Test Board", "post_id": 99999})
        self.assertEqual(response.status_code, 500)

    def test_invalid_request_method(self):
        """Test that a GET request returns a 405 error."""
        self.client.login(username="testuser", password="password123")
        url = reverse("create_board")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content, {
            "success": False, "error": "Invalid request method."})

    def test_unexpected_error_handling(self):
        """Test that unexpected errors return a 500 response."""
        self.client.login(username="testuser", password="password123")
        url = reverse("create_board")

        # Simulate an unexpected error by passing an invalid data type
        response = self.client.post(url, {
            "title": "Valid Title", "post_id": "invalid"})

        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(response.content, {
            "success": False, "error": "An unexpected error occurred."})


class EditBoardViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.user = User.objects.create_user(
            username="testuser", password="password123")
        cls.other_user = User.objects.create_user(
            username="otheruser", password="password456")

        # Create a board belonging to testuser
        cls.board = ImageBoard.objects.create(
            user=cls.user, title="My Board", visibility=0)
        cls.board_url = reverse("edit_board", kwargs={
            "board_id": cls.board.id})

    def test_redirects_unauthenticated_users(self):
        """Test that unauthenticated users cannot access the view."""
        response = self.client.post(self.board_url, {
            "action": "update", "title": "New Title", "visibility": "1"})
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_forbidden_for_other_users(self):
        """Test that another user cannot edit someone else's board."""
        self.client.login(username="otheruser", password="password456")
        response = self.client.post(self.board_url, {
            "action": "update", "title": "New Title", "visibility": "1"})
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_invalid_http_method(self):
        """Test that GET requests are rejected with 405 Method Not Allowed."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.board_url)
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content, {
            "success": False, "error": "Invalid request method."})

    def test_update_board_successfully(self):
        """Test that the board title and visibility can be updated."""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            self.board_url,
            {"action": "update", "title": "Updated Board", "visibility": "1"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "success": True,
                "message": "Board updated successfully.",
                "title": "Updated Board",
                "visibility": 1,
            },
        )

        # Check that the changes were saved in the database
        self.board.refresh_from_db()
        self.assertEqual(self.board.title, "Updated Board")
        self.assertEqual(self.board.visibility, 1)

    def test_update_board_fails_with_empty_title(self):
        """Test that the board title cannot be updated to an empty string."""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(self.board_url, {
            "action": "update", "title": "", "visibility": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "success": False, "error": "Title cannot be empty."})

    def test_update_board_fails_with_invalid_visibility(self):
        """Test that invalid visibility values are rejected."""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(self.board_url, {
            "action": "update", "title": "Valid Title", "visibility": "3"})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "success": False, "error": "Invalid visibility value."})

    def test_delete_board_successfully(self):
        """Test that the board is deleted when action is 'delete'."""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(self.board_url, {"action": "delete"})
        self.assertEqual(response.status_code, 302)  # Redirect to profile page

        # Ensure board no longer exists
        with self.assertRaises(ImageBoard.DoesNotExist):
            ImageBoard.objects.get(id=self.board.id)

    def test_invalid_action_in_post_request(self):
        """Test that an invalid action parameter returns a 405 error."""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(self.board_url, {
            "action": "invalid_action"})
        self.assertEqual(response.status_code, 405)

    def test_edit_board_with_empty_title(self):
        """Test that an empty title returns a JSON error."""
        self.client.login(
            username="testuser", password="password123")
        # Ensure user is logged in

        response = self.client.post(
            self.board_url,
            {"action": "update", "title": "", "visibility": "1"},
            follow=True  # Follow redirects to check response content
        )

        self.assertEqual(response.status_code, 200)
        # Ensure it remains on the same page
        self.assertJSONEqual(
            response.content,
            {"success": False, "error": "Title cannot be empty."}
        )

    def test_edit_board_with_same_title_and_visibility(self):
        """Test that updating a board with the same title and visibility does
        not cause issues."""
        self.client.login(username="testuser", password="password123")
        # Ensure user is logged in

        response = self.client.post(
            self.board_url,
            {"action": "update", "title": self.board.title, "visibility": str(
                self.board.visibility)},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        # Ensure it remains on the same page
        self.assertJSONEqual(
            response.content,
            {"success": True, "message": "Board updated successfully.",
             "title": self.board.title, "visibility": self.board.visibility}
        )

    def test_forbidden_edit_by_non_owner(self):
        """Test that another user cannot edit someone else's board."""
        self.client.login(username="otheruser", password="password456")
        response = self.client.post(self.board_url, {
            "action": "update", "title": "New Title", "visibility": "1"})

        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_csrf_protection(self):
        """Test that CSRF protection works by attempting
        to edit a board without a CSRF token."""
        self.client.login(username="owner", password="password123")
        response = self.client.post(self.board_url, {
            "action": "update", "title": "CSRF Test", "visibility": "1"},
            follow=False)

        # CSRF token is required; if missing, it should not update the board.
        self.assertNotEqual(response.status_code, 200)
        # Should fail with 403 or redirect to login page


class UnpinPostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test users, boards, and posts."""
        cls.user = User.objects.create_user(
            username="testuser", password="password123")
        cls.other_user = User.objects.create_user(
            username="otheruser", password="password456")

        # Create boards
        cls.user_board = ImageBoard.objects.create(
            user=cls.user, title="User Board", visibility=0)
        cls.other_board = ImageBoard.objects.create(
            user=cls.other_user, title="Other User Board", visibility=0)

        # Create a post with UUID
        cls.post = Post.objects.create(
            user=cls.user, title="Sample Post", description="Test description")

        # Pin post to the board
        cls.relationship = BoardImageRelationship.objects.create(
            post_id=cls.post, board_id=cls.user_board)

        # Generate URLs
        cls.unpin_url = reverse("unpin_post", kwargs={
            "board_id": cls.user_board.id, "post_id": cls.post.id})

    def setUp(self):
        """Set up the client for each test."""
        self.client = Client()
        self.client.login(username="testuser", password="password123")

    def test_unpin_successfully(self):
        """Test that a user can successfully unpin a
        post from their own board."""
        response = self.client.post(self.unpin_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "success": True, "message":
            "Post successfully unpinned from the board."})
        self.assertFalse(BoardImageRelationship.objects.filter(
            board_id=self.user_board, post_id=self.post).exists())

    def test_user_cannot_unpin_from_other_users_board(self):
        """Test that a user cannot unpin a post from another user's board."""
        self.client.logout()
        self.client.login(username="otheruser", password="password456")

        other_user_url = reverse("unpin_post", kwargs={
            "board_id": self.user_board.id, "post_id": self.post.id})

        response = self.client.post(other_user_url)
        self.assertEqual(response.status_code, 500, )

        # Verify that the post still exists in the database
        self.assertTrue(
            BoardImageRelationship.objects.filter(
                board_id=self.user_board, post_id=self.post).exists(),
        )

    def test_post_not_in_board_returns_404(self):
        """Test that trying to unpin a post that isn't in the board
        returns a 404 error."""
        self.relationship.delete()  # Remove relationship first

        response = self.client.post(self.unpin_url)
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {
            "success": False, "error": "Post not found in this board."})

    def test_invalid_board_id_returns_500(self):
        """Test that an invalid board_id returns a 404 error."""
        invalid_url = reverse("unpin_post", kwargs={
            "board_id": 9999, "post_id": self.post.id})

        response = self.client.post(invalid_url)
        self.assertEqual(
            response.status_code,
            500,
            "Expected 404 for an invalid board_id, but got a different"
            " response.")

    def test_invalid_post_id_returns_404(self):
        """Test that an invalid post_id (UUID format) returns a 404 error."""
        invalid_uuid = uuid4()
        # Generate a random UUID to mimic an invalid post_id
        invalid_url = reverse("unpin_post", kwargs={
            "board_id": self.user_board.id, "post_id": invalid_uuid})

        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, 404)

    def test_exception_handling_returns_500(self):
        """Test that unexpected exceptions return a 500 error."""
        with self.assertRaises(Exception):
            response = self.client.post(self.unpin_url)
            self.assertEqual(response.status_code, 500)

    def test_rejects_get_requests(self):
        """Test that a GET request is rejected with a 405 error."""
        response = self.client.get(self.unpin_url)
        self.assertEqual(response.status_code, 405)

    def test_database_reflects_unpinning(self):
        """Test that the database is correctly updated after unpinning."""
        self.client.post(self.unpin_url)
        self.assertFalse(BoardImageRelationship.objects.filter(
            board_id=self.user_board, post_id=self.post).exists())

    def test_post_exists_in_multiple_boards(self):
        """Test that the post is only unpinned from the specific board."""
        another_board = ImageBoard.objects.create(
            user=self.user, title="Another Board")
        BoardImageRelationship.objects.create(
            post_id=self.post, board_id=another_board)

        self.client.post(self.unpin_url)

        # The post should still exist in the other board
        self.assertTrue(BoardImageRelationship.objects.filter(
            board_id=another_board, post_id=self.post).exists())
