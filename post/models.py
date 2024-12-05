from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
import uuid

# Create your models here.
class Post(models.Model):
    """
    Stores a single image post related to: model:`auth.User`.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = CloudinaryField('image', default='placeholder', blank=False)
    title = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="uploader")
    likes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} | posted by {self.user} on {self.created_on}"


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
    body = models.CharField(max_length=280)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment: {self.body} by {self.author}"