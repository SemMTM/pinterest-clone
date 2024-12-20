from django.contrib import admin
from .models import Profile, ImageBoard, BoardImageRelationship

# Register your models here.

admin.site.register(Profile)
admin.site.register(ImageBoard)
admin.site.register(BoardImageRelationship)
