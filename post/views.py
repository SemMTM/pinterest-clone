from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator
from .models import Post

# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.all()
    template_name = "post/index.html"
    paginate_by = 6
    context_object_name = "userimages"

    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return "post/image-list.html"
        else:
            return self.template_name