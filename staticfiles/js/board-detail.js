document.addEventListener('DOMContentLoaded', () => {
    // Open Edit Board Modal
    const openEditBoardModalBtn = document.getElementById('open-edit-board-modal-btn');
    const editBoardModal = document.getElementById('edit-board-modal');
    const deleteConfirmationModal = document.getElementById('delete-confirmation-modal');
    const editBoardForm = document.getElementById('edit-board-form');
    const editBoardVisibilitySelect = document.getElementById('edit-board-visibility');

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

    // Update Board Title and Visibility
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
                    visibility: formData.get('visibility'), // Include visibility in the request
                }),
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Failed to update the board.');
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.success) {
                        const boardTitleElement = document.getElementById('board-title');
                        if (boardTitleElement) {
                            boardTitleElement.textContent = formData.get('title');
                        }

                        const boardVisibilityElement = document.getElementById('board-visibility');
                        if (boardVisibilityElement) {
                            boardVisibilityElement.textContent =
                                formData.get('visibility') === '0' ? 'Public' : 'Private';
                        }

                        editBoardModal.classList.add('hidden');
                        alert(data.message);
                    } else {
                        alert(data.error || 'An error occurred.');
                    }
                })
                .catch((error) => console.error('Error updating board:', error));
        });
    }

    //Unpin image functions
    const unpinModal = document.getElementById('unpin-modal');
    const unpinConfirmBtn = document.getElementById('unpin-confirm-btn');
    const unpinCancelBtn = document.getElementById('unpin-cancel-btn');
    const csrfToken = getCookie('csrftoken');
    let currentImageId = null;
    let currentBoardId = null;

    // Add event listeners to all unpin buttons
    document.addEventListener('click', (event) => {
        if (event.target.classList.contains('unpin-btn')) {
            currentImageId = event.target.getAttribute('data-image-id');
            currentBoardId = event.target.getAttribute('data-board-id');
            unpinModal.classList.remove('hidden');
        }
    });

    // Close the modal when the cancel button is clicked
    unpinCancelBtn.addEventListener('click', () => {
        unpinModal.classList.add('hidden');
        currentImageId = null; // Clear the current image ID
        currentBoardId = null; // Clear the current board ID
    });

    // Handle unpin confirmation
    unpinConfirmBtn.addEventListener('click', () => {
        if (!currentImageId || !currentBoardId) {
            alert("Invalid image or board ID.");
            return;
        }

        fetch(`/profile/board/${currentBoardId}/unpin/${currentImageId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to unpin the post.');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Remove the unpinned post from the DOM dynamically
                    const postElement = document.querySelector(`.grid-item[data-post-id="${currentImageId}"]`);
                    if (postElement) {
                        postElement.remove(); // Remove the grid item directly from the DOM
                    }
    
                    unpinModal.classList.add('hidden'); // Hide the modal
                    currentImageId = null; // Clear the current image ID
                    currentBoardId = null; // Clear the current board ID
    
                    // Display a success alert
                    alert('Post removed successfully!');
                } else {
                    alert(data.error || 'An error occurred while unpinning the post.');
                }
            })
            .catch(error => {
                console.error('Error unpinning the post:', error);
            });
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