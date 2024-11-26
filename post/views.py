from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator
from .models import Post

# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.all()
    template_name = "post/index.html"


def homepage(request):
    page_number = request.GET.get('page', 1)
    queryset = Paginator(Post.objects.all(), 3)
    page_obj = queryset.get_page(page_number)

    return render(request, 
            "post/index.html", 
            {'page_obj' : page_obj},
            )