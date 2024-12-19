from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, JsonResponse
from django.template.loader import render_to_string
from post.models import Post
from .models import Profile



def profile_page(request, username):
    user = get_object_or_404(User.objects.filter(username__iexact=username))

    if username != user.username.lower():
        return redirect('profile_page', username=user.username.lower())

    profile, created = Profile.objects.get_or_create(user=user)

    return render(
        request,
        "profile_page/profile_page.html",
        {"profile": profile},
    )


def created_pins(request, username):
    # Fetch the user using the username case-insensitively
    user = get_object_or_404(User.objects.filter(username__iexact=username))

    # Fetch posts created by the user
    created_posts = Post.objects.filter(user=user).order_by('-created_on')

    # Pagination logic
    page_number = request.GET.get('page', 1)
    paginator = Paginator(created_posts, 6)  # Paginate by 6 items per page

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        return HttpResponse("") 

    return render(request, 'profile_page/created_pins.html', {'created_posts': page, 'profile_user': user})