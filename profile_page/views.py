from django.shortcuts import render, get_object_or_404
from .models import Profile

# Create your views here.

def profile_page(request):
    return render(
        request,
        "profile_page/profile_page.html",
    )