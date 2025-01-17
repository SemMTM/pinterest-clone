from django.shortcuts import render, get_object_or_404, reverse, redirect, reverse
from django.views import generic
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Prefetch
from profile_page.models import ImageBoard, BoardImageRelationship
from .models import Post, Comment, ImageTagRelationships, ImageTags
from .forms import CommentForm, PostForm
import json
from profile_page.models import Profile

# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.all()
    template_name = "post/index.html"
    paginate_by = 10
    context_object_name = "userimages"

    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return "post/image_list.html"
        else:
            return self.template_name


def post_detail(request, id):
    queryset = Post.objects.all().select_related('user__profile')
    post = get_object_or_404(queryset, id=id)
    comments = post.comments.select_related('author__profile').order_by("-created_on")
    comment_count = post.comments.count()
    user_boards = ImageBoard.objects.filter(user=request.user) if request.user.is_authenticated else []
    comment_form = CommentForm()
    tags = ImageTags.objects.filter(image_tag__post_id=post)

    return render(
        request,
        "post/post_details.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
            "user_boards": user_boards,
            "tags": tags,
        },
    )

@login_required
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


@require_POST
@login_required
def add_comment(request, post_id):
    """
    Handles adding a new comment to a post via an AJAX request.
    """
    post = get_object_or_404(Post, id=post_id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Ensure it's an AJAX request
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            # Return JSON response
            return JsonResponse({
                'success': True,
                'body': comment.body,
                'author': comment.author.username,
                'created_on': comment.created_on.strftime('%Y-%m-%d %H:%M:%S'),
                'redirect_url': reverse('post_detail', kwargs={'id': post.id}),
            })

        return JsonResponse({'error': 'Invalid form data'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def comment_delete(request, post_id, comment_id):
    """
    Delete an individual comment.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.
    ``comment``
        A single comment related to the post.
    """
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)

    if comment.author == request.user or post.user == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted!')
    else:
        messages.error(request, 'You can only delete your own comments!')

    return redirect('post_detail', id=post.id)


@login_required
def update_comment(request, post_id, comment_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)

    if comment.author != request.user:
        return JsonResponse({'error': 'You are not authorized to edit this comment.'}, status=403)

    try:
        data = json.loads(request.body)
        updated_body = data.get('body', '').strip()

        if not updated_body:
            return JsonResponse({'error': 'Comment body cannot be empty.'}, status=400)

        comment.body = updated_body
        comment.save()

        return JsonResponse({
            'success': True,
            'body': comment.body,
            'redirect_url': reverse('post_detail', kwargs={'id': post.id}),
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    except Exception:
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        post.delete()
        return redirect('home')  

    return redirect('post_detail', id=post_id)


def like_post(request, id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=id)

        if isinstance(request.user, AnonymousUser):
            return JsonResponse({"success": False, "error": "You need to log in to like this post."}, status=401)

        user = request.user

        if user in post.liked_by.all():
            post.liked_by.remove(user)  # Unlike the post
            post.likes -= 1
            liked = False
        else:
            post.liked_by.add(user)  # Like the post
            post.likes += 1
            liked = True

        post.save()

        return JsonResponse({"success": True, "liked": liked, "likes_count": post.likes})

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)