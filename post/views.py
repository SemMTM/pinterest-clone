from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Comment, ImageTagRelationships, ImageTags
from .forms import CommentForm, PostForm

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
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', id=post.id)
    else:
        comment_form = CommentForm()

    return render(
        request,
        "post/post_details.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )


def create_post(request):
    post_form = PostForm()
    if request.method == 'POST':
        post_form = PostForm(data=request.POST, files=request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()

            selected_tags = post_form.cleaned_data['tags']

            for tag in selected_tags:
                ImageTagRelationships.objects.create(post_id=post, tag_name=tag)
                # Create relationships for each selected tag

            messages.success(request, "Your post has been created successfully!")

            return redirect('create_post')

    return render(
        request,
        "post/post_create.html",
        {"post_form": post_form},
    )


def tag_suggestions(request):
    query = request.GET.get('q', '')
    if query:
        # Filter tags containing the query
        tags = ImageTags.objects.filter(tag_name__icontains=query)[:10]  # Limit to 10 results
    else:
        tags = ImageTags.objects.all()[:10]

    data = [{"id": tag.pk, "tag_name": tag.tag_name} for tag in tags]
    return JsonResponse(data, safe=False)