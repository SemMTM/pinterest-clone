from django.urls import path
from .views import CustomLoginView, CustomSignupView, custom_logout

app_name = 'custom_accounts'

urlpatterns = [
    path('login-modal/', CustomLoginView.as_view(), name='login_modal'),
    path('signup-modal/', CustomSignupView.as_view(), name='signup_modal'),
    path('logout/', custom_logout, name='logout'),
]