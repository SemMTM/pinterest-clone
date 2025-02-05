from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.dispatch import receiver
from django.db.models import Count
from django.db.models.signals import post_save
from django.http import (
    Http404, HttpResponse, JsonResponse, HttpResponseForbidden
    )
from post.models import Post
from .models import Profile, ImageBoard, BoardImageRelationship
from .forms import ProfileForm


def profile_page(request, username):
    """
    Displays a user's profile page and ensures the correct username format.

    **Models Used:**
    - `auth.User`: Retrieves the user object based on the provided `username`.
    - `profile_page.Profile`: Ensures the user has an associated profile.
    - `post.ImageBoard`: Ensures the user has an "All Pins" board.
    - `post.Post`: Retrieves posts saved to any of the user's boards.
    - `profile_page.BoardImageRelationship`: Associates posts with the
      "All Pins" board.

    **Templates Rendered:**
    - `"profile_page/profile_page.html"`

    **Returned Variables in Context:**
    - `profile`: The `Profile` instance associated with the user.

    **Functionality:**
    - Fetches the `User` object whose username matches
      `username` (case-insensitive).
    - If the username is not in lowercase, redirects to the correct
      lowercase version.
    - Ensures the `Profile` model exists for the user.
    - Ensures the user has an `"All Pins"` board.
    - If the `"All Pins"` board was just created:
      - Retrieves all unique posts pinned to any of the user’s boards.
      - Associates each post with the `"All Pins"` board.
    - Renders the profile page template with the user's profile data.
    """
    user = get_object_or_404(User.objects.filter(username__iexact=username))

    if username != user.username.lower():
        return redirect('profile_page', username=user.username.lower())

    profile, created = Profile.objects.get_or_create(user=user)

    all_pins_board, created = ImageBoard.objects.get_or_create(
        user=user,
        title="All Pins",
        visibility=1
    )

    if created:
        # Add all posts saved to any board into the "All Pins" board
        saved_posts = Post.objects.filter(
            pinned_image__board_id__user=user
        ).distinct()  # Collect unique posts across all boards
        for post in saved_posts:
            BoardImageRelationship.objects.get_or_create(
                post_id=post,
                board_id=all_pins_board
            )

    return render(
        request,
        "profile_page/profile_page.html",
        {"profile": profile},
    )


def created_pins(request, username):
    """
    Displays a paginated list of posts created by a specific user.

    **Models Used:**
    - `auth.User`: Retrieves the user object based on the provided `username`.
    - `post.Post`: Fetches posts created by the user.

    **Templates Rendered:**
    - `"profile_page/created_pins.html"`

    **Returned Variables in Context:**
    - `created_posts`: A paginated list of `Post` objects created by the user,
      ordered by `created_on` (newest first).
    - `profile_user`: The `User` object whose posts are being displayed.

    **Functionality:**
    - Fetches the `User` object whose username matches `username`
      (case-insensitive).
    - Retrieves all posts created by the user, ordered by `created_on`
      in descending order.
    - Implements pagination:
      - Fetches the page number from the `GET` parameters.
      - Uses Django's `Paginator` to paginate posts, displaying 10 per page.
      - If the requested page exceeds available pages,
        returns an empty `200 OK` response.
    - Renders the `"profile_page/created_pins.html"`
      template with the paginated posts.

    **Pagination Handling:**
    - Default page size: `10` posts per page.
    - If the `page` parameter exceeds available pages, an empty `HttpResponse`
      is returned.
    """
    # Fetch the user using the username case-insensitively
    user = get_object_or_404(User.objects.filter(username__iexact=username))

    # Fetch posts created by the user
    created_posts = Post.objects.filter(user=user).order_by('-created_on')

    # Pagination logic
    page_number = request.GET.get('page', 1)
    paginator = Paginator(created_posts, 10)

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        return HttpResponse("", status=200)

    return render(request, 'profile_page/created_pins.html', {
        'created_posts': page, 'profile_user': user})


def image_boards(request, username):
    """
    Displays a user's image boards, including their
    "All Pins" board, if accessible.

    **Models Used:**
    - `post.User`: Retrieves the user object based on the provided `username`.
    - `profile_page.ImageBoard`: Fetches the user's boards, including
      "All Pins" if accessible.
    - `profile_page.BoardImageRelationship`: Retrieves up to 3 images
      associated with each board.

    **Templates Rendered:**
    - `"profile_page/image_boards.html"`

    **Returned Variables in Context:**
    - `boards_with_images`: A list of dictionaries,
      where each dictionary contains:
      - `board`: An `ImageBoard` instance representing the board.
      - `images`: A queryset of up to 3 `BoardImageRelationship`
        objects associated with the board.
      - `image_count`: The total number of images in the board.

    **Functionality:**
    - Fetches the `User` object whose username matches `username`
      (case-insensitive).
    - Calls `sync_all_pins_board(user)` to ensure the "All Pins"
      board is updated.
    - Fetches the `"All Pins"` board and other image boards:
      - If the request user is the profile owner:
        - Retrieves all boards, including `"All Pins"`.
      - If the request user is not the profile owner:
        - Retrieves only public (`visibility=0`) boards.
    - Annotates boards with an `image_count` field,
      representing the number of images.
    - Collects up to 3 images per board from `BoardImageRelationship`.
    - Renders the `"profile_page/image_boards.html"` template
      with the `boards_with_images` context.

    **Access Permissions:**
    - If the request user owns the profile, they can see all their boards.
    - If the request user does not own the profile, they
      can only see public boards.
    """
    user = get_object_or_404(User.objects.filter(username__iexact=username))

    sync_all_pins_board(user)

    # Fetch "All Pins" board if it's public or the user owns the profile
    if request.user == user:
        # retreives all ImageBoard objects that match the varibles,
        # add an image_count variable with .annotate then returns the
        # .first() matching object
        all_pins_board = ImageBoard.objects.filter(
            user=user, title="All Pins").annotate(
            image_count=Count('image_board_id')).first()

        other_boards = ImageBoard.objects.filter(
            user=user).annotate(image_count=Count(
                'image_board_id')).exclude(title="All Pins")
    else:
        all_pins_board = ImageBoard.objects.filter(
            user=user, title="All Pins", visibility=0
        ).annotate(image_count=Count('image_board_id')).first()

        other_boards = ImageBoard.objects.filter(
            user=user, visibility=0).annotate(
                image_count=Count('image_board_id')).exclude(title="All Pins")

    boards = [all_pins_board] + list(
        other_boards) if all_pins_board else list(other_boards)

    # Fetch up to 3 images for each board
    boards_with_images = []
    for board in boards:
        images = BoardImageRelationship.objects.filter(
            board_id=board).select_related('post_id')[:3]
        boards_with_images.append({
            'board': board,
            'images': images,
            'image_count': board.image_count,
        })

    return render(request,
                  'profile_page/image_boards.html',
                  {'boards_with_images': boards_with_images
                   })


def board_detail(request, board_id):
    """
    Displays the details of a specific image board,
    including its associated images.

    **Models Used:**
    - `profile_page.ImageBoard`: Retrieves the board by `board_id`.
    - `profile_page.BoardImageRelationship`: Fetches images
      associated with the board.

    **Templates Rendered:**
    - `"profile_page/board_detail.html"`

    **Returned Variables in Context:**
    - `board`: The `ImageBoard` instance representing the requested board.
    - `images`: A queryset of `BoardImageRelationship`
      objects containing posts linked to the board.

    **Functionality:**
    - Retrieves the `ImageBoard` instance using `board_id`.
    - Checks the board's visibility:
      - If the board is private (`visibility == 1`) and the
        request user is **not** the board owner,
        raises an `Http404` error.
    - Fetches all images associated with the board
      using `BoardImageRelationship`
      and selects related `Post` objects for efficiency.
    - Renders the `"profile_page/board_detail.html"` template
      with the board and its images.

    **Access Permissions:**
    - Public boards (`visibility == 0`) are accessible to all users.
    - Private boards (`visibility == 1`) are only accessible to
      the board owner.
    - Unauthorized access to a private board results in an `Http404` response.
    """
    board = get_object_or_404(ImageBoard, id=board_id)

    if board.visibility == 1 and request.user != board.user:
        raise Http404

    images = BoardImageRelationship.objects.filter(
        board_id=board).select_related('post_id')

    return render(request, 'profile_page/board_detail.html', {
        'board': board,
        'images': images
        })


def sync_all_pins_board(user):
    """
    Ensures the "All Pins" board contains all posts saved to any
    of the user's boards.

    **Models Used:**
    - `profile_page.ImageBoard`: Retrieves or creates the "All Pins"
      board for the user.
    - `post.Post`: Collects all posts saved to any of the user's boards.
    - `profile_page.BoardImageRelationship`: Establishes relationships
      between posts and the "All Pins" board.

    **Functionality:**
    - Retrieves or creates the "All Pins" board for the given user.
    - Queries all `Post` objects that are pinned to any of the user's boards.
    - Ensures each of these posts is also pinned to the "All Pins" board:
      - If a post is not already in "All Pins", a new
        `BoardImageRelationship` is created.
      - Uses `get_or_create` to prevent duplicate entries.

    **Use Case:**
    - Keeps the "All Pins" board in sync with the user's
      saved posts across all boards.
    - Ensures that posts saved to multiple boards
      are still uniquely tracked in "All Pins."
    """
    all_pins_board, _ = ImageBoard.objects.get_or_create(
        user=user, title="All Pins")

    # Collect all saved posts across all boards
    saved_posts = Post.objects.filter(
        pinned_image__board_id__user=user
    ).distinct()

    # Add posts not already in "All Pins"
    for post in saved_posts:
        BoardImageRelationship.objects.get_or_create(
            post_id=post,
            board_id=all_pins_board
        )


@receiver(post_save, sender=BoardImageRelationship)
def handle_post_save(sender, instance, **kwargs):
    """
    Ensures that a post is added to the "All Pins"
    board whenever it is saved to any board.

    **Models Used:**
    - `profile_page.BoardImageRelationship`: The sender of the
    `post_save` signal.
    - `auth.User`: Retrieves the owner of the board where the post was saved.
    - `profi9le_page.ImageBoard`: Ensures that the "All Pins" board is updated.

    **Functionality:**
    - Retrieves the user associated with the board where the post was saved.
    - Calls `sync_all_pins_board(user)` to update the "All Pins" board.
    - Ensures that any post added to a board is also reflected in "All Pins."

    **Use Case:**
    - Keeps the "All Pins" board in sync whenever a post is added
      to any other board.
    - Automates the process of maintaining a comprehensive board
      of all saved posts.
    """
    user = instance.board_id.user
    sync_all_pins_board(user)


@login_required
def save_to_board(request, post_id):
    """
    Handles saving a post to a specified board via an AJAX request.

    **Models Used:**
    - `post.Post`: Retrieves the post to be saved.
    - `profile_page.ImageBoard`: Fetches the board where
      the post will be saved.
    - `profile_page.BoardImageRelationship`: Creates a relationship
      between the post and the selected board.

    **Expected Request:**
    - A `POST` request containing the `board_id` in `request.POST`.
    - The user must be authenticated.

    **Returned Data (JSON Response):**
    - On success:
      {
          "success": true,
          "message": "Post Saved!"
      }
    - On failure:
      - If `board_id` is missing:
        {
            "success": false,
            "message": "No board selected."
        }
        (HTTP 400 Bad Request)

      - If the request method is not `POST`:
        {
            "success": false,
            "message": "Invalid request method."
        }
        (HTTP 405 Method Not Allowed)

    **Functionality:**
    - Retrieves the `Post` object by `post_id`.
    - Ensures the request is a `POST` request.
    - Retrieves the `board_id` from the request data.
    - If no `board_id` is provided, returns a `400 Bad Request` JSON response.
    - Fetches the `ImageBoard` object that belongs to the authenticated user.
    - Creates a `BoardImageRelationship` entry to link the post to
      the selected board.
    - Returns a JSON response indicating success.

    **Permissions:**
    - Only authenticated users (`@login_required`) can save posts to boards.
    - Users can only save posts to their own boards.
    """
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        board_id = request.POST.get('board_id')
        if not board_id:
            return JsonResponse({
                'success': False,
                'message': 'No board selected.'},
                status=400)

        board = get_object_or_404(ImageBoard, id=board_id, user=request.user)
        BoardImageRelationship.objects.get_or_create(
            post_id=post, board_id=board)
        return JsonResponse({'success': True, 'message': 'Post Saved!'})

    # If accessed via GET or invalid method
    return JsonResponse({'success': False,
                         'message': 'Invalid request method.'},
                        status=405)


@login_required
def create_board(request):
    """
    Handles the creation of a new board and optionally saves a post to it.

    **Models Used:**
    - `profile_page.ImageBoard`: Creates or retrieves a board for the
      authenticated user.
    - `post.Post`: Retrieves the post to be added to the newly created board.
    - `profile_page.BoardImageRelationship`: Establishes a relationship
      between the post and the board.

    **Expected Request:**
    - A `POST` request containing:
      - `title` (required): The name of the new board.
      - `post_id` (optional): The ID of the post to be saved to the board.
    - The user must be authenticated.

    **Returned Data (JSON Response):**
    - On success:
      {
          "success": true,
          "message": "Board created successfully!"
      }
    - On failure:
      - If `title` is missing:
        {
            "success": false,
            "error": "Board title is required."
        }
        (HTTP 400 Bad Request)

      - If a board with the same title already exists:
        {
            "success": false,
            "error": "A board with the title 'Example Title' already exists."
        }
        (HTTP 400 Bad Request)

      - If an unexpected error occurs:
        {
            "success": false,
            "error": "An unexpected error occurred."
        }
        (HTTP 500 Internal Server Error)

      - If the request method is not `POST`:
        {
            "success": false,
            "error": "Invalid request method."
        }
        (HTTP 405 Method Not Allowed)

    **Functionality:**
    - Ensures the request is a `POST` request.
    - Retrieves and trims the `title` field from the request data.
    - Retrieves the `post_id` if provided.
    - If `title` is missing, returns a `400 Bad Request` response.
    - Retrieves the `Post` object using `post_id` (if provided).
    - Attempts to create a new `ImageBoard` for the authenticated user:
      - If the board already exists, returns an error response.
      - If a new board is created, associates the `post_id` (if provided)
        with the board via `BoardImageRelationship`.
    - Returns a success message upon successful board creation.

    **Permissions:**
    - Only authenticated users (`@login_required`) can create boards.
    - Users can only create boards for their own account.
    """
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '').strip()
            post_id = request.POST.get('post_id')

            if not title:
                return JsonResponse({'success': False,
                                     'error': 'Board title is required.'},
                                    status=400)

            post = get_object_or_404(Post, id=post_id)

            board, created = ImageBoard.objects.get_or_create(
                user=request.user, title=title)
            if not created:
                error_message = (
                    f'A board with the title "{title}" '
                    'already exists.'
                )
                return JsonResponse({'success': False, 'error': error_message},
                                    status=400)

            # Create the relationship if the board was created successfully
            BoardImageRelationship.objects.create(post_id=post, board_id=board)
            return JsonResponse({'success': True,
                                 'message': 'Board created successfully!'})

        except Exception:
            # Handle unexpected errors
            return JsonResponse({'success': False,
                                 'error': 'An unexpected error occurred.'},
                                status=500)

    return JsonResponse({'success': False,
                         'error': 'Invalid request method.'},
                        status=405)


@login_required
def edit_board(request, board_id):
    """
    Handles updating or deleting an image board.

    **Models Used:**
    - `profile_page.ImageBoard`: Retrieves and updates or deletes
    the specified board.

    **Expected Request:**
    - A `POST` request containing:
      - `action` (required): Specifies whether to update or delete the board.
        - `"update"`: Updates the board's title and visibility.
        - `"delete"`: Deletes the board.
      - `title` (required for update): The new title of the board.
      - `visibility` (required for update): The new visibility status
        (`"0"` for public, `"1"` for private).

    **Returned Data (JSON Response):**
    - On successful update:
      {
          "success": true,
          "message": "Board updated successfully.",
          "title": "New Board Title",
          "visibility": 0
      }
    - On successful deletion:
      - Redirects to the user's profile page (`profile_page`).

    - On failure:
      - If the user is not the board owner:
        {
            "success": false,
            "error": "You are not allowed to edit this board."
        }
        (HTTP 403 Forbidden)

      - If `title` is empty:
        {
            "success": false,
            "error": "Title cannot be empty."
        }
        (HTTP 400 Bad Request)

      - If `visibility` is invalid:
        {
            "success": false,
            "error": "Invalid visibility value."
        }
        (HTTP 400 Bad Request)

      - If the request method is not `POST`:
        {
            "success": false,
            "error": "Invalid request method."
        }
        (HTTP 405 Method Not Allowed)

    **Functionality:**
    - Ensures the user is authenticated (`@login_required`).
    - Retrieves the `ImageBoard` instance by `board_id`.
    - Verifies that the logged-in user is the owner of the board.
    - If `POST` request:
      - If `action == "update"`:
        - Validates and updates the board's title and visibility.
      - If `action == "delete"`:
        - Deletes the board and redirects to the profile page.
    - If the request method is not `POST`, returns a `405 Method Not Allowed`
      response.

    **Permissions:**
    - Only the board's owner can update or delete it.
    - Unauthorized users receive a `403 Forbidden` response.
    """
    board = get_object_or_404(ImageBoard, id=board_id)

    # Check if the logged-in user is the creator of the board
    if board.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this board.")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update":
            new_title = request.POST.get("title", "").strip()
            new_visibility = request.POST.get("visibility")

            if not new_title:
                return JsonResponse({"success": False,
                                     "error": "Title cannot be empty."})

            if new_visibility not in ["0", "1"]:
                return JsonResponse({"success": False,
                                     "error": "Invalid visibility value."})

            board.title = new_title
            board.visibility = int(new_visibility)
            board.save()

            return JsonResponse({
                "success": True,
                "message": "Board updated successfully.",
                "title": board.title,
                "visibility": board.visibility,
            })

        elif action == "delete":
            board.delete()
            return redirect('profile_page', username=request.user.username)

    return JsonResponse({"success": False,
                         "error": "Invalid request method."},
                        status=405)


@login_required
def unpin_post(request, board_id, post_id):
    """
    Handles removing a post from a specific board.

    **Models Used:**
    - `profile_page.ImageBoard`: Retrieves the board by `board_id` to
      ensure ownership.
    - `profile_page.BoardImageRelationship`: Identifies and deletes the
    relationship between the post and the board.

    **Expected Request:**
    - A `POST` request.
    - The user must own the board from which the post is being unpinned.

    **Returned Data (JSON Response):**
    - On success:
      {
          "success": true,
          "message": "Post successfully unpinned from the board."
      }

    - On failure:
      - If the post is not found in the board:
        {
            "success": false,
            "error": "Post not found in this board."
        }
        (HTTP 404 Not Found)

      - If an unexpected error occurs:
        {
            "success": false,
            "error": "Error message"
        }
        (HTTP 500 Internal Server Error)

      - If the request method is not `POST`:
        {
            "success": false,
            "error": "Invalid request method."
        }
        (HTTP 405 Method Not Allowed)

    **Functionality:**
    - Ensures the request user is authenticated (`@login_required`).
    - Retrieves the `ImageBoard` by `board_id`, ensuring it belongs
      to the logged-in user.
    - Checks if the specified `post_id` exists in the board
      via `BoardImageRelationship`.
    - If found, deletes the relationship, effectively unpinning the post
      from the board.
    - Returns a success response or an appropriate error message.

    **Permissions:**
    - Only the owner of the board can unpin posts from it.
    - Unauthorized access is prevented by filtering the board
      by `user=request.user`.
    """
    if request.method == "POST":
        try:
            # Ensure the board belongs to the user
            board = get_object_or_404(ImageBoard,
                                      id=board_id, user=request.user)

            # Ensure the post exists in the board
            relationship = BoardImageRelationship.objects.filter(
                board_id=board, post_id__id=post_id).first()
            if not relationship:
                return JsonResponse({"success": False,
                                     "error": "Post not found in this board."
                                     },
                                    status=404)

            # Remove the post from the board
            relationship.delete()

            return JsonResponse({
                "success": True,
                "message": "Post successfully unpinned from the board."
                })
        except Exception as e:
            return JsonResponse({"success": False,
                                 "error": str(e)},
                                status=500)

    return JsonResponse({"success": False,
                         "error": "Invalid request method."},
                        status=405)


@login_required
def edit_profile(request):
    """
    Handles editing a user's profile.

    **Models Used:**
    - `Profile`: Retrieves the user's profile for editing.

    **Templates Rendered:**
    - `"profile_page/edit_profile_modal.html"` (for GET requests).

    **Expected Request:**
    - A `POST` request containing profile data and optionally#
      a new profile image.
    - The user must be authenticated.

    **Returned Data:**
    - On successful update:
      ```json
      {
          "success": true,
          "message": "Profile updated successfully.",
          "data": {
              "about": "User's bio",
              "first_name": "First Name",
              "last_name": "Last Name",
              "profile_image": "https://image.url"
          }
      }
      ```

    - On failure (e.g., invalid form data):
      ```json
      {
          "success": false,
          "error": "Invalid data."
      }
      ```

    **Functionality:**
    - Ensures the user is authenticated (`@login_required`).
    - Retrieves the `Profile` instance for the logged-in user.
    - If the request is `POST`:
      - Processes `ProfileForm` with submitted data and files.
      - If valid, saves the profile and returns a success JSON response
        with updated profile details.
      - If invalid, returns a `400 Bad Request` JSON response
        with an error message.
    - If the request is `GET`, renders the `edit_profile_modal.html` template.

    **Permissions:**
    - Only the logged-in user can edit their own profile.
    """
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Profile updated successfully.',
                'data': {
                    'about': profile.about,
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'profile_image': profile.profile_image.url,
                },
            })
        return JsonResponse({'success': False, 'error': 'Invalid data.'})

    return render(request, 'profile_page/edit_profile_modal.html',
                  {'profile': profile})
