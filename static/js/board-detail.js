document.addEventListener('DOMContentLoaded', () => {
    // Open Edit Board Modal
    const openEditBoardModalBtn = document.getElementById('open-edit-board-modal-btn');
    const editBoardModal = document.getElementById('edit-board-modal');
    const deleteConfirmationModal = document.getElementById('delete-confirmation-modal');

    if (openEditBoardModalBtn) {
        openEditBoardModalBtn.addEventListener('click', () => {
            editBoardModal.classList.remove('hidden');
        });
    }

    // Close Edit Board Modal
    const cancelEditBoardBtn = document.getElementById('cancel-edit-board-btn');
    if (cancelEditBoardBtn) {
        cancelEditBoardBtn.addEventListener('click', () => {
            editBoardModal.classList.add('hidden');
        });
    }

    // Open Delete Confirmation Modal
    const deleteBoardBtn = document.getElementById('delete-board-btn');
    if (deleteBoardBtn) {
        deleteBoardBtn.addEventListener('click', () => {
            editBoardModal.classList.add('hidden'); // Hide edit modal
            deleteConfirmationModal.classList.remove('hidden'); // Show delete confirmation modal
        });
    }

    // Close Delete Confirmation Modal
    const cancelDeleteBoardBtn = document.getElementById('cancel-delete-board-btn');
    if (cancelDeleteBoardBtn) {
        cancelDeleteBoardBtn.addEventListener('click', () => {
            deleteConfirmationModal.classList.add('hidden');
        });
    }

    // Confirm Delete
    const confirmDeleteBoardBtn = document.getElementById('confirm-delete-board-btn');
    if (confirmDeleteBoardBtn) {
        confirmDeleteBoardBtn.addEventListener('click', () => {
            // Action to delete the board can be added here
            alert('Board deleted!');
            deleteConfirmationModal.classList.add('hidden');
        });
    }
});