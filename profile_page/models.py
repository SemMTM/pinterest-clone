from django.db import models
from django.contrib.auth.models import User
from django.core.validators import ValidationError
from cloudinary.models import CloudinaryField
from pathlib import Path
import cloudinary
from post.models import Post
from post.utils import compress_and_convert_to_jpeg


VISIBILITY = ((0, "Public"), (1, "Private"))
MAX_FILE_SIZE_MB = 2  # Maximum file size in MB
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']


def validate_image(value):
    """ Custom validator to handle both CloudinaryResource and
    new file uploads. """
    # Skip validation for existing Cloudinary images
    if isinstance(value, str) or hasattr(value, 'public_id'):
        return

    # Validate file extension
    extension = Path(value.name).suffix[1:].lower()  # Extract file extension
    if extension not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"Invalid file type: {extension}. Allowed: {', '.join(
                ALLOWED_EXTENSIONS)}")

    # Validate file size
    file_size_mb = value.size / (1024 * 1024)  # Convert bytes to MB
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise ValidationError(f"File size exceeds {MAX_FILE_SIZE_MB}MB limit.")


class Profile(models.Model):
    """
    Stores details about a user for their public profile, related to:
    model:`auth.User`.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    about = models.TextField(max_length=600, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    profile_image = CloudinaryField(
        'image',
        default='https://res.cloudinary.com/dygztovba/image/upload/v1736352521/wmj7j0gxfg9rch8chlfl.jpg',  # noqa
        blank=False,
        validators=[validate_image]
    )

    def __str__(self):
        return f"Profile for user: {self.user}"

    def save(self, *args, **kwargs):
        """ Override save method to compress and convert
        images before saving. """
        if self.profile_image:
            # Check if profile image is a Cloudinary resource or a local file
            if isinstance(
                self.profile_image,
                cloudinary.CloudinaryResource) or "res.cloudinary.com" in str(
                    self.profile_image):
                pass
            else:
                self.profile_image = compress_and_convert_to_jpeg(
                    self.profile_image)  # Compress local uploads

        super().save(*args, **kwargs)  # Save the model


class ImageBoard(models.Model):
    """
    Stores details about an image board created by a user, related to:
    model:`auth.User`
    """
    title = models.CharField(max_length=90, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="board_creator")
    visibility = models.IntegerField(choices=VISIBILITY, default=0)

    def is_all_pins(self):
        return self.title == "All Pins"

    def __str__(self):
        return f"Image Board of user: {self.user}. Title:{self.title}"


class BoardImageRelationship(models.Model):
    """
    Stores a single entry relationship between a post and a board, related to:
    model:`post.Post` and model:`profile_page.ImageBoard`
    """
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="pinned_image")
    board_id = models.ForeignKey(
        ImageBoard, on_delete=models.CASCADE, related_name="image_board_id")

    class Meta:
        unique_together = ('post_id', 'board_id')
