from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


# Custom error handlers
def custom_403_view(request, exception):
    return render(request, "errors/403.html", status=403)


def custom_404_view(request, exception):
    return render(request, "errors/404.html", status=404)


def custom_500_view(request):
    return render(request, "errors/500.html", status=500)


handler403 = custom_403_view
handler404 = custom_404_view
handler500 = custom_500_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('profile/', include("profile_page.urls"), name="profile-urls"),
    path('custom-accounts/', include("custom_auth.urls",
                                     namespace="custom_accounts")),
    path("", include("post.urls"), name="post-urls"),
]
