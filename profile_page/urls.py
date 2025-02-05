from django.urls import path
from . import views

urlpatterns = [
    path('create-board/', views.create_board, name='create_board'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('<str:username>/', views.profile_page, name='profile_page'),
    path('<str:username>/created/', views.created_pins, name='created_pins'),
    path('<str:username>/boards/', views.image_boards, name='image_boards'),
    path('board/<int:board_id>/', views.board_detail, name='board_detail'),
    path('board/<int:board_id>/edit/', views.edit_board, name='edit_board'),
    path('board/<int:board_id>/unpin/<uuid:post_id>/', views.unpin_post,
         name='unpin_post'),
    path('save-to-board/<uuid:post_id>/', views.save_to_board,
         name='save_to_board'),
]
