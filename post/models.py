from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
import uuid
from .utils import compress_and_convert_to_jpeg


def validate_image_size(image):
    """
    Validator for max file size on image uploaded to: model:`post.Post`
    """
    max_size = 20 * 1024 * 1024  # 20MB in bytes
    if image.size > max_size:
        raise ValidationError("The uploaded image exceeds the maximum "
                              "file size of 20MB.")


class Post(models.Model):
    """
    Stores a single image post related to: model:`auth.User`.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = CloudinaryField('image', blank=False,
                            validators=[
                                        FileExtensionValidator
                                        (allowed_extensions=[
                                            'jpg', 'jpeg', 'png', 'webp']),
                                        validate_image_size])
    title = models.CharField(max_length=100, blank=False, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="uploader")
    description = models.TextField(max_length=300, blank=True)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_posts",
                                      blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """ Override save method to compress and convert images
        before saving only when new image is uploaded."""
        if self.pk is None or (self.image and hasattr(self.image, "file")):
            self.image = compress_and_convert_to_jpeg(self.image)

        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Store a single comment on a post related to: model:`post.Post`
    and model:`auth.User`
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter"
    )
    body = models.TextField(max_length=600)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment: '{self.body}' by {self.author}"


class ImageTags(models.Model):
    """
    Stores a single image tag related to: model: `post.Post`
    """
    tag_name = models.CharField(
        primary_key=True,
        max_length=200,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9 \-]+$',
                message="Tag name must contain only letters, "
                        "digits, spaces, and hyphens.",
                code='invalid_tag_name'
            )
        ])

    def save(self, *args, **kwargs):
        if self.tag_name:
            self.tag_name = self.tag_name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tag_name


class ImageTagRelationships(models.Model):
    """
    Stores an entry of the tag and which post it is paired with, related to:
    model: `post.Post` and model: `post.ImageTags`
    """
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_id")
    tag_name = models.ForeignKey(
        ImageTags, on_delete=models.CASCADE, related_name="image_tag")
