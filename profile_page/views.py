from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.dispatch import receiver
from django.db.models import Count
from django.db.models.signals import post_save, post_delete
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from post.models import Post
from .models import Profile, ImageBoard, BoardImageRelationship
from .forms import ProfileForm



def profile_page(request, username):
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

    if request.user == user:
        boards = ImageBoard.objects.filter(user=user)
    else:
        boards = ImageBoard.objects.filter(user=user, visibility=0)

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
    paginator = Paginator(created_posts, 10) 

    try:
        page = paginator.page(page_number)
    except EmptyPage: 
        return HttpResponse("", status=200) 

    return render(request, 'profile_page/created_pins.html', {'created_posts': page, 'profile_user': user})


def image_boards(request, username):
    user = get_object_or_404(User.objects.filter(username__iexact=username))

    sync_all_pins_board(user)

    # Fetch "All Pins" board if it's public or the user owns the profile
    if request.user == user:
        all_pins_board = ImageBoard.objects.filter(user=user, title="All Pins").annotate(image_count=Count('image_board_id')).first()
        other_boards = ImageBoard.objects.filter(user=user).annotate(image_count=Count('image_board_id')).exclude(title="All Pins")
    else:
        all_pins_board = ImageBoard.objects.filter(
            user=user, title="All Pins", visibility=0
        ).annotate(image_count=Count('image_board_id')).first()
        other_boards = ImageBoard.objects.filter(user=user, visibility=0).annotate(image_count=Count('image_board_id')).exclude(title="All Pins")

    boards = [all_pins_board] + list(other_boards) if all_pins_board else list(other_boards)

    # Fetch up to 3 images for each board
    boards_with_images = []
    for board in boards:
        images = BoardImageRelationship.objects.filter(board_id=board).select_related('post_id')[:3]
        boards_with_images.append({
            'board': board,
            'images': images,
            'image_count': board.image_count,
        })

    return render(request, 'profile_page/image_boards.html', {'boards_with_images': boards_with_images})


def board_detail(request, board_id):
    board = get_object_or_404(ImageBoard, id=board_id)

    if board.visibility == 1 and request.user != board.user:
        raise Http404

    images = BoardImageRelationship.objects.filter(board_id=board).select_related('post_id')

    return render(request, 'profile_page/board_detail.html', {
        'board': board, 
        'images': images
        })


def sync_all_pins_board(user):
    """Ensures the 'All Pins' board contains all posts saved to any board."""
    all_pins_board, _ = ImageBoard.objects.get_or_create(user=user, title="All Pins")
    
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
    """Add a post to 'All Pins' if it's saved to any board."""
    user = instance.board_id.user
    sync_all_pins_board(user)


@login_required
def save_to_board(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        board_id = request.POST.get('board_id')
        if not board_id:
            return JsonResponse({'success': False, 'message': 'No board selected.'}, status=400)
        
        board = get_object_or_404(ImageBoard, id=board_id, user=request.user)
        BoardImageRelationship.objects.get_or_create(post_id=post, board_id=board)
        return JsonResponse({'success': True, 'message': 'Post Saved!'})

    # If accessed via GET or invalid method
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)


@login_required 
def create_board(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '').strip()
            post_id = request.POST.get('post_id')

            if not title:
                return JsonResponse({'success': False, 'error': 'Board title is required.'}, status=400)

            post = get_object_or_404(Post, id=post_id)

            board, created = ImageBoard.objects.get_or_create(user=request.user, title=title)
            if not created:
                error_message = f'A board with the title "{title}" already exists.'
                return JsonResponse({'success': False, 'error': error_message}, status=400)

            # Create the relationship if the board was created successfully
            BoardImageRelationship.objects.create(post_id=post, board_id=board)
            return JsonResponse({'success': True, 'message': 'Board created successfully!'})

        except Exception as e:
            # Handle unexpected errors
            return JsonResponse({'success': False, 'error': 'An unexpected error occurred.'}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)



@login_required
def edit_board(request, board_id):
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
                return JsonResponse({"success": False, "error": "Title cannot be empty."})

            if new_visibility not in ["0", "1"]:
                return JsonResponse({"success": False, "error": "Invalid visibility value."})

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

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)


@login_required
def unpin_post(request, board_id, post_id):
    if request.method == "POST":
        try:
            # Ensure the board belongs to the user
            board = get_object_or_404(ImageBoard, id=board_id, user=request.user)

            # Ensure the post exists in the board
            relationship = BoardImageRelationship.objects.filter(board_id=board, post_id__id=post_id).first()
            if not relationship:
                return JsonResponse({"success": False, "error": "Post not found in this board."}, status=404)

            # Remove the post from the board
            relationship.delete()

            return JsonResponse({"success": True, "message": "Post successfully unpinned from the board."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)


@login_required
def edit_profile(request):
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
    
    return render(request, 'profile_page/edit_profile_modal.html', {'profile': profile})