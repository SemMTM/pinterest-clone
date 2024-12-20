from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
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
    boards = ImageBoard.objects.filter(user=user)

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
