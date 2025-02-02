from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('profile/', include("profile_page.urls"), name="profile-urls"),
    path('custom-accounts/', include("custom_auth.urls",
                                     namespace="custom_accounts")),
    path("", include("post.urls"), name="post-urls"),
]
