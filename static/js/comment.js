document.addEventListener('DOMContentLoaded', function() {
    // Comment modal functions
    const commentIcon = document.getElementById('comment-icon');
    const commentModal = document.getElementById('comment-modal');
    const closeModal = document.getElementById('close-modal');
    const openCommentModal = document.getElementById('open-comment-modal')
    const viewAll = document.getElementById('view-all')
    const commentForm = document.getElementById('commentForm');
    const commentInput = commentForm.querySelector('textarea[name="body"]');
    const commentIdInput = document.getElementById('edit-comment-id');

    function openModal() {
        commentModal.classList.add('modal-show');
    }
    function closeTheModal() {
        commentModal.classList.remove('modal-show');
    }
    if (commentIcon) {
        commentIcon.addEventListener('click', () => {
        openModal();
        commentInput.value = ''; // Clear the textarea
        commentIdInput.value = ''; // Reset the hidden input for a new comment
        });
    }
    if (viewAll) {
        viewAll.addEventListener('click', openModal);
    }
    if (openCommentModal) {
        openCommentModal.addEventListener('click', openModal);
    }
    if (closeModal) {
        closeModal.addEventListener('click', closeTheModal);
    }
    commentModal.addEventListener('click', function(e) {
        if (e.target === commentModal) {
            closeTheModal();
        }
    });


    // Delete comment functions
    const deleteModal = document.getElementById('delete-comment-modal'); // Delete confirmation modal
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn'); // Confirm delete button
    const cancelDeleteBtn = document.getElementById('cancel-delete-btn'); // Cancel delete button

    let deleteUrl = null; // URL to delete the comment

    // Attach click event to all delete buttons
    document.querySelectorAll('.comment-close-btn').forEach(button => {
        button.addEventListener('click', function () {
            deleteUrl = `/${this.getAttribute('post_id')}/delete_comment/${this.getAttribute('comment_id')}/`; // Construct delete URL
            deleteModal.classList.remove('hidden'); // Show the modal
        });
    });
    // Confirm delete action
    confirmDeleteBtn.addEventListener('click', function () {
        if (deleteUrl) {
            window.location.href = deleteUrl; // Redirect to the delete URL
        }
    });
    // Cancel delete action
    cancelDeleteBtn.addEventListener('click', function () {
        deleteModal.classList.add('hidden'); // Hide the modal
        deleteUrl = null; // Clear the delete URL
    });


    // Edit button functionality
    const commentsContainer = document.getElementById('comments-container');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Populate the form with the comment to edit
    commentsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('edit-comment-btn')) {
            commentInput.value = e.target.dataset.commentBody;
            commentIdInput.value = e.target.dataset.commentId;
        }
    });

    // Handle comment form submission
    commentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
    
        const updatedBody = commentInput.value.trim();
        const commentId = commentIdInput.value; // Check if it's an edit
        const postId = commentsContainer.dataset.postId;
    
        if (!updatedBody) {
            alert("Comment body can't be empty.");
            return;
        }
    
        try {
            let url, payload, headers;
    
            if (commentId) {
                // Update existing comment
                url = `/${postId}/update_comment/${commentId}/`;
                headers = {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                };
                payload = JSON.stringify({ body: updatedBody });
            } else {
                // Add new comment
                url = `/${postId}/add_comment/`;
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                };
                payload = new URLSearchParams({
                    body: updatedBody,
                    csrfmiddlewaretoken: csrfToken,
                }).toString();
            }
    
            const response = await fetch(url, {
                method: 'POST',
                headers,
                body: payload,
            });
    
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Failed to submit comment: ${errorText}`);
            }
    
            const data = await response.json();
    
            if (commentId) {
                // Update comment in DOM
                const commentBodySpan = commentsContainer.querySelector(`[data-comment-id="${commentId}"] .comment-body`);
                if (commentBodySpan) commentBodySpan.textContent = data.body;
            } else {
                // Add new comment (reload or dynamic rendering)
                window.location.href = data.redirect_url;
            }
    
            // Clear form
            commentInput.value = '';
            commentIdInput.value = '';
        } catch (error) {
            console.error('Error submitting comment:', error);
            alert('Failed to submit comment.');
        }
    });

    // Utility function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});