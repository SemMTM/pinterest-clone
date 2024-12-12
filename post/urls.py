from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:id>/', views.post_detail, name='post_detail'),
    path('create_post', views.create_post, name='create_post')
]