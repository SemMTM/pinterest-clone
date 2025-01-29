import { showPopUpMessage } from './pop_up.js'

document.addEventListener('DOMContentLoaded', () => {
    // Open Edit Board Modal
    const openEditBoardModalBtn = document.getElementById('open-edit-board-modal-btn');
    const editBoardModal = document.getElementById('edit-board-modal');
    const editBoardForm = document.getElementById('edit-board-form');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    const editBoardModalContent = document.getElementsByClassName("board-modal-content")[0];

    if (openEditBoardModalBtn) {
        openEditBoardModalBtn.addEventListener('click', () => {
            editBoardModal.classList.add('modal-show');
            editBoardModalContent.classList.add('board-modal-content-visible');
        });
    }

    // Close Edit Board Modal
    const cancelEditBoardBtn = document.getElementById('cancel-edit-board-btn');
    if (cancelEditBoardBtn) {
        cancelEditBoardBtn.addEventListener('click', () => {
            editBoardModal.classList.remove('modal-show');
            editBoardModalContent.classList.remove('board-modal-content-visible');
        });
    }
    
    // Open Delete Confirmation Modal
    const deleteConfirmationModal = document.getElementById('delete-confirmation-modal');
    const deleteBoardBtn = document.getElementById('delete-board-btn');
    
    if (deleteBoardBtn) {
        deleteBoardBtn.addEventListener('click', () => {
            editBoardModal.classList.remove('modal-show');
            deleteConfirmationModal.classList.remove('hidden'); 
            deleteConfirmationModal.classList.add('visible');

        });
    }

    // Close Delete Confirmation Modal
    const cancelDeleteBoardBtn = document.getElementById('cancel-delete-board-btn');
    if (cancelDeleteBoardBtn) {
        cancelDeleteBoardBtn.addEventListener('click', () => {
            deleteConfirmationModal.classList.remove('visible');
            editBoardModalContent.classList.remove('board-modal-content-visible');
        });
    }

    // Confirm Delete
    const confirmDeleteBoardBtn = document.getElementById('confirm-delete-board-btn');
    if (confirmDeleteBoardBtn) {
        confirmDeleteBoardBtn.addEventListener('click', () => {
            showPopUpMessage('Board deleted!');
            deleteConfirmationModal.classList.add('hidden');
        });
    }

    // Submit on enter
    if (editBoardForm) {
        editBoardForm.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) { // Prevents new line on Enter + Shift
                event.preventDefault(); // Prevents default newline behavior
                editBoardForm?.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
            }
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
                    'X-CSRFToken': csrfToken,
                },
                body: new URLSearchParams({
                    action: 'update',
                    title: formData.get('title'),
                    visibility: formData.get('visibility'), 
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
                        showPopUpMessage(data.message);
                    } else {
                        showPopUpMessage(data.error || 'An error occurred.');
                    }
                })
                .catch((error) => showPopUpMessage('Error updating board'));
        });
    }

    //Unpin image functions
    const unpinModal = document.getElementById('unpin-modal');
    const unpinConfirmBtn = document.getElementById('unpin-confirm-btn');
    const unpinCancelBtn = document.getElementById('unpin-cancel-btn');
    let currentImageId = null;
    let currentBoardId = null;

    // Add event listeners to all unpin buttons
    document.addEventListener('click', (event) => {
        if (event.target.classList.contains('unpin-btn')) {
            currentImageId = event.target.getAttribute('data-image-id');
            currentBoardId = event.target.getAttribute('data-board-id');
            unpinModal.classList.remove('unpin-modal-hidden');
            unpinModal.classList.add('unpin-modal-visible');
        }
    });

    // Close the modal when the cancel button is clicked
    unpinCancelBtn.addEventListener('click', () => {
        unpinModal.classList.add('unpin-modal-hidden');
        unpinModal.classList.remove('unpin-modal-visible');
        currentImageId = null; 
        currentBoardId = null; 
    });

    // Handle unpin confirmation
    unpinConfirmBtn.addEventListener('click', () => {
        if (!currentImageId || !currentBoardId) {
            showPopUpMessage("Invalid image or board ID.");
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
    
                    unpinModal.classList.add('hidden'); 
                    currentImageId = null; 
                    currentBoardId = null; 
                    showPopUpMessage('Post removed successfully!');
                } else {
                    showPopUpMessage('An error occurred while unpinning the post.');
                }
            })
            .catch(error => {
                showPopUpMessage('Error unpinning the post:');
            });
    });
});