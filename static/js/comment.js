import { showPopUpMessage } from './pop_up.js';

document.addEventListener('DOMContentLoaded', () => {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    // Comment Modal Elements 
    const commentModal = document.getElementById('comment-modal');
    const commentIcon = document.getElementById('comment-icon');
    const closeModal = document.getElementById('close-modal');
    const viewAll = document.getElementById('view-all');
    const commentForm = document.getElementById('commentForm');
    const commentInput = commentForm?.querySelector('textarea[name="body"]');
    const commentIdInput = document.getElementById('edit-comment-id');

    // Helper to reset comment form
    const resetCommentForm = () => {
        if (commentInput) commentInput.value = '';
        if (commentIdInput) commentIdInput.value = '';
    };

    // Show/Hide Comment Modal
    if (commentIcon) {
        commentIcon.addEventListener('click', () => {
            commentModal?.classList.add('modal-show');
            resetCommentForm();

            if (commentInput) {
                setTimeout(() => commentInput.focus(), 0);
            }
        });
    }

    if (closeModal) {
        closeModal.addEventListener('click', () => {
            commentModal?.classList.remove('modal-show');
        });
    }

    if (viewAll) {
        viewAll.addEventListener('click', () => {
            commentModal?.classList.add('modal-show');

            if (commentInput) {
                setTimeout(() => commentInput.focus(), 0);
            }
        });
    }


    // Delete Comment Modal
    const deleteModal = document.getElementById('delete-comment-modal');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    const cancelDeleteBtn = document.getElementById('cancel-delete-btn');
    let deleteUrl = null;

    document.querySelectorAll('.comment-close-btn').forEach((button) => {
        button.addEventListener('click', () => {
            deleteUrl = `/${button.getAttribute('post_id')}/delete_comment/${button.getAttribute('comment_id')}/`;
            deleteModal?.classList.remove('hidden');
        });
    });

    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', () => {
            if (deleteUrl) window.location.href = deleteUrl;
        });
    }

    if (cancelDeleteBtn) {
        cancelDeleteBtn.addEventListener('click', () => {
            deleteModal?.classList.add('hidden');
            deleteUrl = null;
        });
    }


    // Edit Comment
    const commentsContainer = document.getElementById('comments-container');

    if (commentsContainer) {
        commentsContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('edit-comment-btn')) {
                commentInput.value = e.target.dataset.commentBody;
                commentIdInput.value = e.target.dataset.commentId;
            }
        });
    }

    if (commentInput) {
        commentInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) { // Prevents new line on Enter + Shift
                event.preventDefault(); // Prevents default newline behavior
                commentForm?.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
            }
        });
    }


    // Comment Form Submission
    if (commentForm) {
        commentForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const body = commentInput?.value.trim();
            const commentId = commentIdInput?.value;
            const postId = commentsContainer?.dataset.postId;

            if (!body) {
                showPopUpMessage('Comment cannot be empty.');
                return;
            }

            const url = commentId ? `/${postId}/update_comment/${commentId}/`
                : `/${postId}/add_comment/`;

            const headers = {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': commentId ? 'application/json' : 'application/x-www-form-urlencoded',
            };

            const payload = commentId ? JSON.stringify({ body })
                : new URLSearchParams({ body, csrfmiddlewaretoken: csrfToken }).toString();
            try {
                const response = await fetch(url, { method: 'POST', headers, body: payload });
                if (!response.ok) {
                    throw new Error('Failed to submit comment.');
                }

                const data = await response.json();

                if (data.success) {
                    if (commentId) {
                        const commentBodySpan = commentsContainer.querySelector(
                            `[data-comment-id="${commentId}"] .comment-body`
                        );
                        if (commentBodySpan) commentBodySpan.textContent = data.body;
                            window.location.href = data.redirect_url;
                    } else {
                        window.location.href = data.redirect_url;
                    }

                    resetCommentForm();
                    showPopUpMessage('Your comment was added successfully!');
                } else {
                    showPopUpMessage(data.error || 'An error occurred.');
                }
            } catch (error) {
                showPopUpMessage('An unexpected error occurred.');
            }
        });
    }


    // Like Button
    const likeButton = document.getElementById('like-button');
    const likeCount = document.getElementById('like-count');

    if (likeButton) {
        likeButton.addEventListener('click', async () => {
            const postId = likeButton.getAttribute('data-post-id');

            try {
                const response = await fetch(`/post/${postId}/like/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                });

                if (response.status === 401) {
                    showPopUpMessage('You need to log in to like a post.');
                    return;
                }

                if (!response.ok) throw new Error('Failed to like the post.');

                const data = await response.json();

                if (data.success) {
                    likeCount.textContent = data.likes_count; // Update like count
                    likeButton.textContent = data.liked ? 'Liked' : 'Like'; // Update button text
                    likeButton.classList.toggle('active', data.liked); // Toggle active class
                } else {
                    showPopUpMessage(data.error || 'An error occurred while liking the post.');
                }
            } catch (error) {
                console.error('Error liking the post:', error);
            }
        });
    }
});
