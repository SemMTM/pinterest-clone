from django.contrib import admin
from .models import Profile, ImageBoard, BoardImageRelationship


admin.site.register(Profile)
admin.site.register(ImageBoard)
admin.site.register(BoardImageRelationship)
