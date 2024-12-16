document.addEventListener('DOMContentLoaded', function() {
    const commentIcon = document.getElementById('comment-icon');
    const commentModal = document.getElementById('comment-modal');
    const closeModal = document.getElementById('close-modal');
    const commentForm = document.getElementById('commentForm');
    const commentInput = commentForm ? commentForm.querySelector('textarea, input[type="text"]') : null;
    const openCommentModal = document.getElementById('open-comment-modal')
    const viewAll = document.getElementById('view-all')

    // Open the modal
    function openModal() {
        commentModal.classList.add('modal-show');
    }

    // Close the modal
    function closeTheModal() {
        commentModal.classList.remove('modal-show');
    }

    // Click on the comment icon to open modal
    if (commentIcon) {
        commentIcon.addEventListener('click', openModal);
    }

    if (viewAll) {
        viewAll.addEventListener('click', openModal);
    }

    if (openCommentModal) {
        openCommentModal.addEventListener('click', openModal);
    }

    // Close modal when the close button is clicked
    if (closeModal) {
        closeModal.addEventListener('click', closeTheModal);
    }

    // Close modal if user clicks outside modal content
    commentModal.addEventListener('click', function(e) {
        if (e.target === commentModal) {
            closeTheModal();
        }
    });
});