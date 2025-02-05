from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.http import require_POST, require_GET
import json
from profile_page.models import ImageBoard
from .models import Post, Comment, ImageTagRelationships, ImageTags
from .forms import CommentForm, PostForm


# Create your views here.
class PostList(generic.ListView):
    """
    View to display a paginated list of posts.

    **Model:**
    - Displays data from the model:`post.Post`.

    **Templates Rendered:**
    - `"post/index.html"` (default template for non-HTMX requests)
    - `"post/image_list.html"` (for HTMX requests)

    **Returned Variables in Context:**
    - `userimages`: A paginated queryset of `Post` objects ordered by the
      `created_on` field in descending order. Retrieved from
      `Post.objects.all()` and managed by Django's built-in pagination.

    **Functionality:**
    - Enforces pagination, limiting results to `10` per page.
    - Checks if the requested page exceeds available pages and
      raises an `Http404`
      error if no more images are available.
    - Dynamically selects the template based on whether the request
      is made via HTMX.
    """
    queryset = Post.objects.all().order_by("-created_on")
    template_name = "post/index.html"
    paginate_by = 10
    context_object_name = "userimages"

    def get_queryset(self):
        queryset = super().get_queryset()
        page = self.request.GET.get("page", 1)

        # Check if the requested page exceeds available pages
        paginator = self.get_paginator(queryset, self.paginate_by)
        if int(page) > paginator.num_pages:
            raise Http404("No more images available.")
        return queryset

    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return "post/image_list.html"
        else:
            return self.template_name


def post_detail(request, id):
    """
    View to display the details of a single post, including comments,
    user boards, and associated tags.

    **Models Used:**
    - `post.Post`: Retrieves the post by its ID, along with its associated user
      and profile.
    - `post.Comment`: Fetches all comments related to the post.
    - `profile_page.Profile`: Accesses the profile of the post author and
      comment authors.
    - `profile_page.ImageBoard`: Retrieves boards associated with the
      authenticated user.
    - `post.ImageTags`: Fetches tags associated with the post.

    **Template Rendered:**
    - `"post/post_details.html"`

    **Returned Variables in Context:**
    - `post`: The requested `Post` object, retrieved using `get_object_or_404`
      from `Post.objects.all().select_related('user__profile')`.
    - `comments`: A queryset of comments related to the post,
      ordered by `created_on`, retrieved via `post.comments.select_related
      ('author__profile')`.
    - `comment_count`: The total number of comments on the post, obtained using
      `post.comments.count()`.
    - `user_boards`: A queryset of `ImageBoard` objects belonging to the
      authenticated user. If the user is not authenticated, an empty list
      is returned.
    - `comment_form`: An instance of `CommentForm` for submitting new comments.
    - `tags`: A queryset of `ImageTags` associated with the post,
      retrieved using `ImageTags.objects.filter(image_tag__post_id=post)`.

    **Functionality:**
    - Fetches a `Post` object by ID, along with its related user profile.
    - Retrieves all comments linked to the post, including their
      authors' profiles.
    - Provides a count of comments on the post.
    - If the user is authenticated, fetches their associated
      `ImageBoard` objects.
    - Retrieves tags associated with the post.
    - Passes all the gathered data to the `"post/post_details.html"` template
      for rendering.
    """
    queryset = Post.objects.all().select_related('user__profile')
    post = get_object_or_404(queryset, id=id)
    comments = post.comments.select_related(
        'author__profile').order_by("created_on")
    comment_count = post.comments.count()
    user_boards = ImageBoard.objects.filter(
        user=request.user) if request.user.is_authenticated else []
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


def create_post(request):
    """
    View to handle post creation, including form submission and
    tag relationships.

    **Models Used:**
    - `post.Post`: Stores the newly created post.
    - `auth.User`: Associates the authenticated user with the post.
    - `post.ImageTagRelationships`: Creates relationships between the post and
      its selected tags.

    **Template Rendered (for GET requests):**
    - `"post/post_create.html"`

    **Returned Variables in Context (for GET requests):**
    - `post_form`: An instance of `PostForm` for submitting a new post.

    **Functionality:**
    - If the request is a `POST` request:
      - Validates and processes the `PostForm`.
      - Saves the post with the currently authenticated user as the owner.
      - Iterates through the selected tags and creates `ImageTagRelationships`
        entries to associate the post with each tag.
      - Returns a JSON response indicating success or failure.
    - If the request is a `GET` request:
      - Renders the `"post/post_create.html"` template with an empty #
        `PostForm`.
    """
    if request.method == 'POST':
        post_form = PostForm(data=request.POST, files=request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()

            selected_tags = post_form.cleaned_data['tags']
            for tag in selected_tags:
                ImageTagRelationships.objects.create(post_id=post,
                                                     tag_name=tag)
                # Create relationships for each selected tag

            return JsonResponse({'success': True, 'message':
                                 "Your post has been created successfully!"})

        return JsonResponse({'success': False,
                             'error': post_form.errors.as_json()}, status=400)

    post_form = PostForm()
    return render(
        request,
        "post/post_create.html",
        {"post_form": post_form},
    )


@require_GET
def tag_suggestions(request):
    """
    View to provide tag suggestions based on user input.

    **Models Used:**
    - `post.ImageTags`: Retrieves tags that match the user's query.

    **Returned Data (JSON Response):**
    - A list of up to 10 tag objects, each represented as a dictionary with:
      - `id`: The primary key of the `ImageTags` object.
      - `tag_name`: The name of the tag.

    **Functionality:**
    - Accepts a GET request with an optional query parameter `q`.
    - If `q` is provided, filters `ImageTags` where `tag_name` contains
      the query (case-insensitive) and limits results to 10.
    - If `q` is not provided, returns the first 10 `ImageTags`.
    - Returns the filtered tag data as a JSON response.

    **Example Response:**
    ```json
    [
        {"id": 1, "tag_name": "nature"},
        {"id": 2, "tag_name": "photography"},
        {"id": 3, "tag_name": "travel"}
    ]
    ```
    """
    query = request.GET.get('q', '')
    if query:
        # Filter tags containing the query
        tags = ImageTags.objects.filter(tag_name__icontains=query)[:10]
    else:
        tags = ImageTags.objects.all()[:10]

    data = [{"id": tag.pk, "tag_name": tag.tag_name} for tag in tags]
    return JsonResponse(data, safe=False)


@require_POST
@login_required
def add_comment(request, post_id):
    """
    Handles adding a new comment to a post via an AJAX request.

    **Models Used:**
    - `post.Post`: Retrieves the post to which the comment is being added.
    - `post.Comment`: Stores the newly created comment.
    - `auth.User`: Associates the authenticated user as the comment author.

    **Expected Request:**
    - A `POST` request containing comment data (`body`).
    - Must be an AJAX request (`x-requested-with` header must be set).
    - The user must be authenticated.

    **Returned Data (JSON Response):**
    - On success:
      ```json
      {
          "success": true,
          "body": "This is a comment",
          "author": "username",
          "created_on": "2025-02-02 12:34:56",
          "redirect_url": "/post/1/"
      }
      ```
      - `success`: Boolean indicating the comment was successfully added.
      - `body`: The content of the new comment.
      - `author`: The username of the comment's author.
      - `created_on`: The timestamp when the comment was created.
      - `redirect_url`: URL to the post detail page.

    - On failure:
      ```json
      {"error": "Invalid form data"}
      ```
      - If the form data is invalid, returns an error message with
        a 400 status code.

      ```json
      {"error": "Invalid request"}
      ```
      - If the request is not an AJAX request, returns an error message
        with a 400 status code.

    **Functionality:**
    - Retrieves the `Post` object by ID.
    - Ensures the request is an AJAX `POST` request.
    - Validates the `CommentForm`.
    - If valid, associates the comment with the authenticated user and
      the post, then saves it.
    - Returns a JSON response with the comment details and a redirect URL.
    - If invalid, returns an appropriate JSON error response.

    **Notes:**
    - Requires the user to be authenticated (`@login_required`).
    - Only accepts `POST` requests (`@require_POST`).
    """
    post = get_object_or_404(Post, id=post_id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Ensure it's an AJAX request
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


@login_required
def comment_delete(request, post_id, comment_id):
    """
    Handles deleting a comment from a post.

    **Models Used:**
    - `post.Post`: Retrieves the post to which the comment belongs.
    - `post.Comment`: Retrieves the specific comment to be deleted.
    - `auth.User`: Used to check if the request user has permission to
      delete the comment.

    **Expected Request:**
    - A request from an authenticated user.
    - The user must be either:
      - The author of the comment.
      - The owner of the post.

    **Functionality:**
    - Retrieves the `Post` object by `post_id`.
    - Retrieves the `Comment` object by `comment_id`, ensuring it belongs to
      the post.
    - Checks if the request user is either:
      - The comment author.
      - The post owner.
    - If authorized, deletes the comment.
    - Redirects the user to the `post_detail` page of the related post.

    **Redirection:**
    - Redirects to `post_detail` using `reverse('post_detail',
      kwargs={'id': post.id})`.

    **Permissions:**
    - Only the comment's author or the post owner can delete the comment.
    - If an unauthorized user attempts deletion, the comment remains unchanged.
    - Requires the user to be authenticated (`@login_required`).
    """
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)

    if comment.author == request.user or post.user == request.user:
        comment.delete()

    return redirect('post_detail', id=post.id)


@login_required
def update_comment(request, post_id, comment_id):
    """
    Handles updating an existing comment via an AJAX request.

    **Models Used:**
    - `post.Post`: Retrieves the post associated with the comment.
    - `post.Comment`: Retrieves the specific comment to be updated.
    - `auth.User`: Used to verify that the request user is the comment author.

    **Expected Request:**
    - A `POST` request containing JSON data.
    - The user must be the author of the comment.

    **Returned Data (JSON Response):**
    - On success:
      ```json
      {
          "success": true,
          "body": "Updated comment text",
          "redirect_url": "/post/1/"
      }
      ```
      - `success`: Boolean indicating the comment was successfully updated.
      - `body`: The updated comment content.
      - `redirect_url`: URL to the post detail page.

    - On failure:
      - If the request method is not `POST`:
        ```json
        {"error": "Invalid request method."}
        ```
        (HTTP 405 Method Not Allowed)

      - If the user is not the comment author:
        ```json
        {"error": "You are not authorized to edit this comment."}
        ```
        (HTTP 403 Forbidden)

      - If the `body` field is empty:
        ```json
        {"error": "Comment body cannot be empty."}
        ```
        (HTTP 400 Bad Request)

      - If the JSON data is malformed:
        ```json
        {"error": "Invalid JSON data."}
        ```
        (HTTP 400 Bad Request)

      - If an unexpected error occurs:
        ```json
        {"error": "Internal Server Error"}
        ```
        (HTTP 500 Internal Server Error)

    **Functionality:**
    - Ensures the request is a `POST` request.
    - Retrieves the `Post` and `Comment` objects, ensuring the comment belongs
      to the post.
    - Validates that the request user is the comment's author.
    - Parses JSON data from the request body and extracts the updated
      comment text.
    - Ensures the comment body is not empty.
    - Updates and saves the comment.
    - Returns a JSON response with the updated comment and a redirect URL.

    **Permissions:**
    - Only the comment's author can edit it.
    - Requires the user to be authenticated (`@login_required`).
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)

    if comment.author != request.user:
        return JsonResponse({'error':
                            'You are not authorized to edit this comment.'},
                            status=403)

    try:
        data = json.loads(request.body)
        updated_body = data.get('body', '').strip()

        if not updated_body:
            return JsonResponse({'error': 'Comment body cannot be empty.'},
                                status=400)

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
    """
    Handles deleting a post.

    **Models Used:**
    - `post.Post`: Retrieves and deletes the specified post.
    - `auth.User`: Ensures that only the post owner can delete the post.

    **Expected Request:**
    - A `POST` request to confirm the deletion.
    - The authenticated user must be the owner of the post.

    **Redirection:**
    - On successful deletion (`POST` request):
      - Redirects to `'home'` (homepage).
    - On an invalid request (e.g., `GET` request):
      - Redirects to `'post_detail'`, displaying the post.

    **Functionality:**
    - Ensures the request user is authenticated (`@login_required`).
    - Retrieves the `Post` object by `post_id`, ensuring the logged-in
      user is the owner.
    - If the request method is `POST`, deletes the post and redirects
      to `'home'`.
    - If the request method is not `POST`, redirects back to the post
      detail page.

    **Permissions:**
    - Only the post owner can delete the post.
    - Unauthorized users cannot access or delete the post.
    """
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        post.delete()
        return redirect('home')

    return redirect('post_detail', id=post_id)


def like_post(request, id):
    """
    Handles deleting a post.

    **Models Used:**
    - `post.Post`: Retrieves and deletes the specified post.
    - `auth.User`: Ensures that only the post owner can delete the post.

    **Expected Request:**
    - A `POST` request to confirm the deletion.
    - The authenticated user must be the owner of the post.

    **Redirection:**
    - On successful deletion (`POST` request):
      - Redirects to `'home'` (homepage).
    - On an invalid request (e.g., `GET` request):
      - Redirects to `'post_detail'`, displaying the post.

    **Functionality:**
    - Ensures the request user is authenticated (`@login_required`).
    - Retrieves the `Post` object by `post_id`, ensuring the logged-in user
      is the owner.
    - If the request method is `POST`, deletes the post and redirects
      to `'home'`.
    - If the request method is not `POST`, redirects back to the post detail
      page.

    **Permissions:**
    - Only the post owner can delete the post.
    - Unauthorized users cannot delete the post.
    """
    if request.method == "POST":
        post = get_object_or_404(Post, id=id)

        if isinstance(request.user, AnonymousUser):
            return JsonResponse({"success": False, "error":
                                "You need to log in to like this post."},
                                status=401)

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

        return JsonResponse({"success": True, "liked": liked, "likes_count":
                             post.likes})

    return JsonResponse({"success": False, "error": "Invalid request method."},
                        status=405)
