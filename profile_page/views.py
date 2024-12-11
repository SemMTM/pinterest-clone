from django.shortcuts import render, get_object_or_404
from .models import Profile

# Create your views here.

def profile_page(request, user):
    queryset = Profile.objects.all()
    profile = get_object_or_404(queryset, user=user)

    return render(
        request,
        "profile_page/profile_page.html",
        {"profile": profile},
    )