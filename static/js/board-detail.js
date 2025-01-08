document.addEventListener('DOMContentLoaded', () => {
    // Open Edit Board Modal
    const openEditBoardModalBtn = document.getElementById('open-edit-board-modal-btn');
    const editBoardModal = document.getElementById('edit-board-modal');
    const deleteConfirmationModal = document.getElementById('delete-confirmation-modal');
    const editBoardForm = document.getElementById('edit-board-form');

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

    // Update Board Title
    if (editBoardForm) {
        editBoardForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(editBoardForm);
            const updateUrl = editBoardForm.getAttribute('action');

            fetch(updateUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: new URLSearchParams({
                    action: 'update',
                    title: formData.get('title'),
                }),
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Failed to update the board title.');
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.success) {
                        const boardTitleElement = document.getElementById('board-title');
                        if (boardTitleElement) {
                            boardTitleElement.textContent = formData.get('title');
                        }
                        editBoardModal.classList.add('hidden');
                        alert(data.message);
                    } else {
                        alert(data.error || 'An error occurred.');
                    }
                })
                .catch((error) => console.error('Error updating board title:', error));
        });
    }

    //Unpin image functions
    const unpinModal = document.getElementById('unpin-modal');
        const unpinConfirmBtn = document.getElementById('unpin-confirm-btn');
        const unpinCancelBtn = document.getElementById('unpin-cancel-btn');
        let currentImageId = null;

        // Add event listeners to all unpin buttons
        document.querySelectorAll('.unpin-btn').forEach(button => {
            button.addEventListener('click', (event) => {
                currentImageId = event.target.getAttribute('data-image-id');
                unpinModal.classList.remove('hidden');
            });
        });

        // Close the modal when the cancel button is clicked
        unpinCancelBtn.addEventListener('click', () => {
            unpinModal.classList.add('hidden');
            currentImageId = null; // Clear the current image ID
        });

        // Placeholder for unpin confirmation
        unpinConfirmBtn.addEventListener('click', () => {
            alert(`Unpinning image ID: ${currentImageId}`);
            unpinModal.classList.add('hidden');
        });
});

// Utility function to get CSRF token
function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find((row) => row.startsWith(name + '='))
        ?.split('=')[1];
    return cookieValue || '';
}