from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from .models import Profile

# Create your views here.

def profile_page(request, user):
    # Checks if user has a profile, if they do not then one is created for them.
    try:
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, user=user)
    except Http404:
        user = request.user
        profile = Profile(
            user=user
        )
        profile.save()

    queryset = Profile.objects.all()

    return render(
        request,
        "profile_page/profile_page.html",
        {"profile": profile},
    )