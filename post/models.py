from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import RegexValidator, FileExtensionValidator
from cloudinary.models import CloudinaryField
import uuid

# Create your models here.
class Post(models.Model):
    """
    Stores a single image post related to: model:`auth.User`.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = CloudinaryField('image', blank=False,
            validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
            )
    title = models.CharField(max_length=100, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="uploader")
    description = models.TextField(blank=True)
    likes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """
    Store a single comment on a post related to: model:`blog.Post` and model:`auth.User`
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter"
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment: '{self.body}' by {self.author}"


class ImageTags(models.Model):
    """
    Stores a single image tag related to: model: `blog.Post`
    """
    tag_name = models.CharField(
        primary_key=True, 
        max_length=200,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9 \-]+$',
                message="Tag name must contain only letters, digits, spaces, and hyphens.",
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
    Stores an entry of the tag and which post it is paired with, related to: model: `blog.Post` and model: `blog.ImageTags`
    """
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_id")
    tag_name = models.ForeignKey(
        ImageTags, on_delete=models.CASCADE, related_name="image_tag")
