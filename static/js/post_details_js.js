document.addEventListener('DOMContentLoaded', function() {
    // Comment modal functions
    const commentIcon = document.getElementById('comment-icon');
    const commentModal = document.getElementById('comment-modal');
    const closeModal = document.getElementById('close-modal');
    const openCommentModal = document.getElementById('open-comment-modal')
    const viewAll = document.getElementById('view-all')

    function openModal() {
        commentModal.classList.add('modal-show');
    }
    function closeTheModal() {
        commentModal.classList.remove('modal-show');
    }
    if (commentIcon) {
        commentIcon.addEventListener('click', openModal);
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


    const commentsContainer = document.getElementById('comments-container');
    const commentInput = document.querySelector('#commentForm textarea[name="body"]');
    const commentIdInput = document.getElementById('edit-comment-id');

    commentsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('edit-comment-btn')) {
            commentInput.value = e.target.dataset.commentBody; // Populate textarea
            commentIdInput.value = e.target.dataset.commentId; // Set comment ID in hidden input
        }
    });
});