from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from post.models import Post

VISIBILITY = ((0, "Public"), (1, "Private"))

class Profile(models.Model):
    """
    Stores details about a user for their public profile, related to: model:`auth.User`.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    about = models.TextField(max_length=600, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    profile_image = CloudinaryField(
        'image', 
        default='https://res.cloudinary.com/dygztovba/image/upload/v1736352521/wmj7j0gxfg9rch8chlfl.jpg', 
        blank=False)
    
    def __str__(self):
        return f"Profile for user: {self.user}"


class ImageBoard(models.Model):
    title = models.CharField(max_length=90, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="board_creator")
    visibility = models.IntegerField(choices=VISIBILITY, default=0)

    def is_all_pins(self):
        return self.title == "All Pins"

    def __str__(self):
        return f"Image Board of user: {self.user}. Title:{self.title}"


class BoardImageRelationship(models.Model):
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="pinned_image")
    board_id = models.ForeignKey(
        ImageBoard, on_delete=models.CASCADE, related_name="image_board_id")

    class Meta:
        unique_together = ('post_id', 'board_id')