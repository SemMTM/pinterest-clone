from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.profile_page, name='profile_page'),
    path('<str:user>/created', views.created_pins, name='created_pins'),
]