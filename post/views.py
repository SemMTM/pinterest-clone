from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.core.paginator import Paginator
from .models import Post

# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.all()
    template_name = "post/index.html"
    paginate_by = 3
    context_object_name = "userimages"

    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return "post/image_list.html"
        else:
            return self.template_name


def post_detail(request, id):
    queryset = Post.objects.all()
    post = get_object_or_404(queryset, id=id)

    return render(
        request,
        "post/post_details.html",
        {"post": post},
    )