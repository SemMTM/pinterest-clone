from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Comment, ImageTags, ImageTagRelationships


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:140px; max-height:'
                           '140px">'.format(obj.image.url))

    list_display = ['title', 'user', 'image_tag', 'created_on']
    list_filter = ['user']


admin.site.register(Comment)
admin.site.register(ImageTags)
admin.site.register(ImageTagRelationships)
