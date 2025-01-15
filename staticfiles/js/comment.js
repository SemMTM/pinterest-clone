document.addEventListener('DOMContentLoaded', () => {
    // Utility Functions
    const getElement = (id) => document.getElementById(id);
    const addEvent = (element, event, handler) => element?.addEventListener(event, handler);
    const toggleClass = (element, className, action) => element?.classList[action](className);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    const resetCommentForm = (commentInput, commentIdInput) => {
        if (commentInput) commentInput.value = '';
        if (commentIdInput) commentIdInput.value = '';
    };

    // Modal Handlers
    const setupModal = (modal, openTriggers, closeTriggers, resetForm = null) => {
        const openModal = () => {
            toggleClass(modal, 'modal-show', 'add');
            if (resetForm) resetForm();
        };
        const closeModal = () => toggleClass(modal, 'modal-show', 'remove');

        openTriggers.forEach(trigger => addEvent(trigger, 'click', openModal));
        closeTriggers.forEach(trigger => addEvent(trigger, 'click', closeModal));

        modal?.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });
    };

    // Comment Modal Setup
    const commentModal = getElement('comment-modal');
    const commentIcon = getElement('comment-icon');
    const closeModal = getElement('close-modal');
    const viewAll = getElement('view-all');
    const commentForm = getElement('commentForm');
    const commentInput = commentForm?.querySelector('textarea[name="body"]');
    const commentIdInput = getElement('edit-comment-id');

    setupModal(
        commentModal,
        [commentIcon, viewAll],
        [closeModal],
        () => resetCommentForm(commentInput, commentIdInput)
    );

    // Delete Comment Modal
    const deleteModal = getElement('delete-comment-modal');
    const confirmDeleteBtn = getElement('confirm-delete-btn');
    const cancelDeleteBtn = getElement('cancel-delete-btn');
    let deleteUrl = null;

    document.querySelectorAll('.comment-close-btn').forEach(button => {
        addEvent(button, 'click', () => {
            deleteUrl = `/${button.getAttribute('post_id')}/delete_comment/${button.getAttribute('comment_id')}/`;
            toggleClass(deleteModal, 'hidden', 'remove');
        });
    });

    addEvent(confirmDeleteBtn, 'click', () => {
        if (deleteUrl) window.location.href = deleteUrl;
    });

    addEvent(cancelDeleteBtn, 'click', () => {
        toggleClass(deleteModal, 'hidden', 'add');
        deleteUrl = null;
    });

    // Edit Comment
    const commentsContainer = getElement('comments-container');
    addEvent(commentsContainer, 'click', (e) => {
        if (e.target.classList.contains('edit-comment-btn')) {
            commentInput.value = e.target.dataset.commentBody;
            commentIdInput.value = e.target.dataset.commentId;
        }
    });

    // Comment Form Submission
    addEvent(commentForm, 'submit', async (e) => {
        e.preventDefault();

        const body = commentInput?.value.trim();
        const commentId = commentIdInput?.value;
        const postId = commentsContainer?.dataset.postId;

        if (!body) {
            alert("Comment body can't be empty.");
            return;
        }

        const url = commentId
            ? `/${postId}/update_comment/${commentId}/`
            : `/${postId}/add_comment/`;
        const headers = {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': commentId ? 'application/json' : 'application/x-www-form-urlencoded',
        };
        const payload = commentId
            ? JSON.stringify({ body })
            : new URLSearchParams({ body, csrfmiddlewaretoken: csrfToken }).toString();

        try {
            const response = await fetch(url, { method: 'POST', headers, body: payload });
            if (!response.ok) throw new Error(await response.text());

            const data = await response.json();
            if (commentId) {
                const commentBodySpan = commentsContainer.querySelector(`[data-comment-id="${commentId}"] .comment-body`);
                commentBodySpan.textContent = data.body;
            } else {
                window.location.href = data.redirect_url;
            }

            resetCommentForm(commentInput, commentIdInput);
        } catch (error) {
            console.error('Error submitting comment:', error);
            alert('Failed to submit comment.');
        }
    });

    const likeButton = document.getElementById('like-button');
    const likeCount = document.getElementById('like-count');

    if (likeButton) {
        likeButton.addEventListener('click', () => {
            if (!document.body.dataset.isAuthenticated) {
                alert('You need to log in to like a post.');
                return;
            }
            
            const postId = likeButton.getAttribute('data-post-id');
            fetch(`/post/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to like the post.');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        likeCount.textContent = data.likes_count; // Update like count
                        likeButton.textContent = data.liked ? 'Liked' : 'Like'; // Update button text
                        likeButton.classList.toggle('active', data.liked); // Toggle active class
                    } else {
                        alert('An error occurred while liking the post.');
                    }
                })
                .catch(error => console.error('Error liking the post:', error));
        });
    }
});
