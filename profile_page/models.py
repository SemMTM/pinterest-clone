from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

# Create your models here.

class Profile(models.Model):
    """
    Stores details about a user for their public profile, related to: model:`auth.User`.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user")
    about = models.TextField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    profile_image = CloudinaryField('image', default='placeholder', blank=False)
    
    def __str__(self):
        return f"Profile for user: {self.user}"