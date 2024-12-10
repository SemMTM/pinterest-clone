from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils.text import slugify
from .models import Profile

# Create your views here.
def profile_page(request):
    return render(
        request,
        "public_profile/profile_page.html",
    )