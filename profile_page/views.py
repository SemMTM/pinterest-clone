from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from post.models import Post
from .models import Profile, ImageBoard, BoardImageRelationship



def profile_page(request, username):
    user = get_object_or_404(User.objects.filter(username__iexact=username))

    if username != user.username.lower():
        return redirect('profile_page', username=user.username.lower())

    profile, created = Profile.objects.get_or_create(user=user)

    all_pins_board, created = ImageBoard.objects.get_or_create(
        user=user,
        title="All Pins"
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
    # Fetch the user using the username case-insensitively
    user = get_object_or_404(User.objects.filter(username__iexact=username))

    # Fetch posts created by the user
    created_posts = Post.objects.filter(user=user).order_by('-created_on')

    # Pagination logic
    page_number = request.GET.get('page', 1)
    paginator = Paginator(created_posts, 6)  # Paginate by 6 items per page

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        return HttpResponse("") 

    return render(request, 'profile_page/created_pins.html', {'created_posts': page, 'profile_user': user})


def image_boards(request, username):
    user = get_object_or_404(User.objects.filter(username__iexact=username))

    sync_all_pins_board(user)

    all_pins_board = ImageBoard.objects.filter(user=user, title="All Pins").first()
    other_boards = ImageBoard.objects.filter(user=user).exclude(title="All Pins")

    boards = [all_pins_board] + list(other_boards)

    # Fetch up to 3 images for each board
    boards_with_images = []
    for board in boards:
        images = BoardImageRelationship.objects.filter(board_id=board).select_related('post_id')[:3]
        boards_with_images.append({
            'board': board,
            'images': images,
        })

    return render(request, 'profile_page/image_boards.html', {'boards_with_images': boards_with_images})


def board_detail(request, board_id):
    board = get_object_or_404(ImageBoard, id=board_id)
    images = BoardImageRelationship.objects.filter(board_id=board).select_related('post_id')

    return render(request, 'profile_page/board_detail.html', {'board': board, 'images': images})


@csrf_exempt
def edit_board(request, board_id):
    board = get_object_or_404(ImageBoard, id=board_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update':
            # Update the board title
            new_title = request.POST.get('title', '').strip()
            if new_title:
                board.title = new_title
                board.save()
                return JsonResponse({'success': True, 'title': board.title})
            return JsonResponse({'success': False, 'error': 'Title cannot be empty'})

        elif action == 'delete':
            # Delete the board
            board.delete()
            return JsonResponse({'success': True, 'redirect_url': reverse('profile_page', args=[request.user.username])})
        
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


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

    # Remove posts from "All Pins" that aren't saved to any other board
    all_pins_posts = BoardImageRelationship.objects.filter(board_id=all_pins_board)
    for relationship in all_pins_posts:
        if not BoardImageRelationship.objects.filter(
            post_id=relationship.post_id
        ).exclude(board_id=all_pins_board).exists():
            relationship.delete()


@receiver(post_save, sender=BoardImageRelationship)
def handle_post_save(sender, instance, **kwargs):
    """Add a post to 'All Pins' if it's saved to any board."""
    user = instance.board_id.user
    sync_all_pins_board(user)


@receiver(post_delete, sender=BoardImageRelationship)
def handle_post_delete(sender, instance, **kwargs):
    """Remove a post from 'All Pins' if it's not saved to any other board."""
    user = instance.board_id.user
    sync_all_pins_board(user)


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