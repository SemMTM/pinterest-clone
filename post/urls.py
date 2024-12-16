from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('create_post/', views.create_post, name='create_post'),
    path('tag-suggestions/', views.tag_suggestions, name='tag_suggestions'),
    path('<slug:id>/', views.post_detail, name='post_detail'),
    path('<slug:post_id>/update_comment/<int:comment_id>/', 
        views.update_comment, name='edit_comment'),
    path('<slug:post_id>/delete_comment/<int:comment_id>/', 
        views.comment_delete, name='delete_comment'),
]