from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, ImageBoard, BoardImageRelationship
from post.models import Post
from profile_page.views import sync_all_pins_board
from unittest.mock import patch
from django.utils.timezone import now, timedelta


class ProfilePageViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="TestUser", password="password123")
        self.client.login(username="TestUser", password="password123")

        # Create a sample post for the user
        self.post = Post.objects.create(
            user=self.user,
            title="Test Post",
            description="This is a test post.",
            image="test_image.jpg"
        )

        # Create a URL for the test user's profile page
        self.url = reverse("profile_page", kwargs={"username": self.user.username.lower()})

    def test_profile_page_exists(self):
        """Test that the profile page loads successfully for an existing user."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_profile_creation_on_page_load(self):
        """Test that a profile is created if it does not exist."""
        self.client.get(self.url)
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_all_pins_board_creation(self):
        """Test that the "All Pins" board is created for the user."""
        self.client.get(self.url)
        self.assertTrue(ImageBoard.objects.filter(user=self.user, title="All Pins").exists())

    def test_all_pins_board_populated_with_saved_posts(self):
        """Test that the 'All Pins' board is populated with saved posts."""
        # Manually associate a post with a board
        board = ImageBoard.objects.create(user=self.user, title="Test Board")
        BoardImageRelationship.objects.create(post_id=self.post, board_id=board)

        # Trigger the view
        self.client.get(self.url)

        # Verify that the post is added to the 'All Pins' board
        all_pins_board = ImageBoard.objects.get(user=self.user, title="All Pins")
        self.assertTrue(BoardImageRelationship.objects.filter(post_id=self.post, board_id=all_pins_board).exists())

    def test_distinct_saved_posts_in_all_pins(self):
        """Test that only distinct saved posts are added to the 'All Pins' board."""
        # Create multiple boards and associate the same post
        board1 = ImageBoard.objects.create(user=self.user, title="Test Board 1")
        board2 = ImageBoard.objects.create(user=self.user, title="Test Board 2")
        BoardImageRelationship.objects.create(post_id=self.post, board_id=board1)
        BoardImageRelationship.objects.create(post_id=self.post, board_id=board2)

        # Trigger the view
        self.client.get(self.url)

        # Verify that the 'All Pins' board contains only one instance of the post
        all_pins_board = ImageBoard.objects.get(user=self.user, title="All Pins")
        self.assertEqual(BoardImageRelationship.objects.filter(post_id=self.post, board_id=all_pins_board).count(), 1)

    
class CreatedPinsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="TestUser", password="password123")
        self.other_user = User.objects.create_user(username="OtherUser", password="password123")
        self.posts = [
            Post.objects.create(
                user=self.user,
                title=f"Post {i}",
                description=f"Description {i}",
                image="test_image.jpg",
                created_on=now() - timedelta(days=i),
            )
            for i in range(15)
        ]

        self.posts = sorted(self.posts, key=lambda x: x.created_on, reverse=True)
        self.url = reverse("created_pins", kwargs={"username": self.user.username})

    def test_created_pins_page_loads(self):
        """Test that the created pins page loads successfully."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile_page/created_pins.html")

    def test_correct_posts_displayed(self):
        """Test that the created pins view displays the correct posts."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        displayed_posts = list(response.context["created_posts"].object_list)
        self.assertQuerySetEqual(
            displayed_posts, 
            [str(post) for post in self.posts[:6]], 
            transform=str
        )

    def test_pagination_functionality(self):
        """Test pagination works as expected."""
        response = self.client.get(f"{self.url}?page=2")
        self.assertEqual(response.status_code, 200)

        # Verify the second page has the correct posts
        displayed_posts = list(response.context["created_posts"].object_list)
        self.assertQuerySetEqual(
            displayed_posts, 
            [str(post) for post in self.posts[6:12]], 
            transform=str
        )

    def test_empty_page_returns_empty_response(self):
        """Test that requesting a non-existent page returns an empty response."""
        response = self.client.get(f"{self.url}?page=100")  # Page number out of range
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"")

    def test_no_posts_for_other_user(self):
        """Test that posts from other users are not displayed."""
        response = self.client.get(reverse("created_pins", kwargs={"username": self.other_user.username}))
        self.assertEqual(response.status_code, 200)
        displayed_posts = list(response.context["created_posts"].object_list)
        self.assertQuerySetEqual(displayed_posts, [])

    def test_case_insensitive_username(self):
        """Test that the view handles case-insensitive usernames."""
        response = self.client.get(reverse("created_pins", kwargs={"username": self.user.username.lower()}))
        self.assertEqual(response.status_code, 200)
        displayed_posts = list(response.context["created_posts"].object_list)
        self.assertQuerySetEqual(
            displayed_posts, 
            [str(post) for post in self.posts[:6]], 
            transform=str
        )


class ImageBoardsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="TestUser", password="password123")
        self.other_user = User.objects.create_user(username="OtherUser", password="password123")

        # Create sample boards for the test user
        self.all_pins_board = ImageBoard.objects.create(user=self.user, title="All Pins")
        self.board1 = ImageBoard.objects.create(user=self.user, title="Travel")
        self.board2 = ImageBoard.objects.create(user=self.user, title="Nature")

        # Create a board for another user
        self.other_user_board1 = ImageBoard.objects.create(user=self.other_user, title="Other Board 1")
        self.other_user_board2 = ImageBoard.objects.create(user=self.other_user, title="Other Board 2")

        # Create posts and pin them to boards
        self.posts = [
            Post.objects.create(
                user=self.user,
                title=f"Post {i}",
                description=f"Description {i}",
                image="test_image.jpg",
                created_on=now()
            )
            for i in range(6)  # Create 6 posts for assigning to boards
        ]

        # Pin some posts to boards
        for i, post in enumerate(self.posts[:3]):  # Pin 3 posts to Travel board
            BoardImageRelationship.objects.create(post_id=post, board_id=self.board1)

        for post in self.posts[3:]:  # Pin remaining posts to Nature board
            BoardImageRelationship.objects.create(post_id=post, board_id=self.board2)

        self.url = reverse("image_boards", kwargs={"username": self.user.username})

    def test_image_boards_page_loads(self):
        """Test that the image boards page loads successfully."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile_page/image_boards.html")

    def test_correct_boards_displayed(self):
        """Test that the correct boards are displayed."""
        response = self.client.get(self.url)
        boards_with_images = response.context["boards_with_images"]

        # Check that the correct number of boards is displayed
        self.assertEqual(len(boards_with_images), 3)

        # Verify board titles
        board_titles = [item["board"].title for item in boards_with_images]
        self.assertIn("All Pins", board_titles)
        self.assertIn("Travel", board_titles)
        self.assertIn("Nature", board_titles)

    def test_board_images_limited_to_three(self):
        """Test that each board displays at most 3 images."""
        response = self.client.get(self.url)
        boards_with_images = response.context["boards_with_images"]

        for board in boards_with_images:
            self.assertLessEqual(len(board["images"]), 3)

    def test_all_pins_board_sync(self):
        """Test that the All Pins board is synchronized."""
        new_post = Post.objects.create(
            user=self.user,
            title="New Post",
            description="Description for new post",
            image="test_image.jpg",
            created_on=now(),
        )

        BoardImageRelationship.objects.create(post_id=new_post, board_id=self.board1)

        # Call sync explicitly
        sync_all_pins_board(self.user)

        all_pins_board_images = BoardImageRelationship.objects.filter(board_id=self.all_pins_board)
        self.assertIn(new_post, [relationship.post_id for relationship in all_pins_board_images])

    def test_case_insensitive_username(self):
        """Test that the view handles case-insensitive usernames."""
        response = self.client.get(reverse("image_boards", kwargs={"username": self.user.username.lower()}))
        self.assertEqual(response.status_code, 200)

    def test_no_boards_for_other_user(self):
        """Test that boards from other users are not displayed."""
        response = self.client.get(reverse("image_boards", kwargs={"username": self.user.username}))
        boards_with_images = response.context["boards_with_images"]

        # Check the boards belong only to self.user
        for board_info in boards_with_images:
            self.assertEqual(board_info["board"].user, self.user)

        # Confirm only user's boards are returned
        self.assertEqual(len(boards_with_images), 3)  # 3 boards for self.user

    def test_nonexistent_user_returns_404(self):
        """Test that a nonexistent user returns a 404 error."""
        response = self.client.get(reverse("image_boards", kwargs={"username": "NonexistentUser"}))
        self.assertEqual(response.status_code, 404)