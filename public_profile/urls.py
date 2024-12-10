from django.urls import path
from . import views

urlpatterns = [
    path('profile-page/', views.ProfileDetailedView.as_view(), name='profile_page'),
]