from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from post.models import Post
from .models import Profile

# Create your views here.

def profile_page(request, username):
    # Fetch the user using a case-insensitive query
    user = get_object_or_404(User.objects.filter(username__iexact=username))

    if username != user.username.lower():
        return redirect('profile_page', username=user.username.lower())

    # Ensure the user has a profile
    profile, created = Profile.objects.get_or_create(user=user)
    
    # Checks if user has a profile, if they do not then one is created for them.
    #try:
    #    queryset = Profile.objects.all()
    #    profile = get_object_or_404(queryset, user=user)
    #except Http404:
    #    user = request.user
    #    profile = Profile(
    #        user=user
    #    )
    #    profile.save()

    #queryset = Profile.objects.all()

    return render(
        request,
        "profile_page/profile_page.html",
        {"profile": profile},
    )


def created_pins(request, user):
    profile_user = get_object_or_404(User, user=user)
    created_posts = Post.objects.filter(user=profile_user).order_by('-created_on')

    return render(request, 'profile_page/created_pins.html', {'created_posts': created_posts})