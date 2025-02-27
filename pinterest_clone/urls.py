from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import JsonResponse


def is_json_request(request):
    """
    Helper function to determine if a request expects a JSON response.
    """
    return (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or "application/json" in request.headers.get("Accept", "")
    )


def custom_403_view(request, exception):
    """
    Custom 403 Forbidden error handler.
    Returns a JSON response for API requests,
    and renders an error page for HTML requests.
    """
    if is_json_request(request):
        return JsonResponse({"error": "Forbidden"}, status=403)

    return render(request, "errors/403.html", status=403)


def custom_404_view(request, exception):
    """
    Custom 404 Not Found error handler.
    Returns a JSON response for API requests,
    and renders an error page for HTML requests.
    """
    if is_json_request(request):
        return JsonResponse({"error": "Not Found"}, status=404)

    return render(request, "errors/404.html", status=404)


def custom_500_view(request):
    """
    Custom 500 Internal Server Error handler.
    Returns a JSON response for API requests,
    and renders an error page for HTML requests.
    """
    if is_json_request(request):
        return JsonResponse({"error": "Internal Server Error"}, status=500)

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
