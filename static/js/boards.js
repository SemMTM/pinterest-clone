document.addEventListener('DOMContentLoaded', function() {
    // Save modal scripts
    const saveButton = document.getElementById('save-btn');
    const modal = document.getElementById('save-to-board-modal');
    const closeModalButton = document.getElementById('close-save-modal');
    const boardButtons = document.querySelectorAll('.save-modal-board-btn');
    const isAuthenticated = saveButton.getAttribute('data-authenticated');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    // Open modal
    saveButton.addEventListener('click', () => {
        if (!isAuthenticated) {
            alert("Log in to save posts");
        } else {
            modal.classList.remove('save-modal-hidden');
            modal.classList.add('save-modal-visible');
        }
    });

    // Close modal
    closeModalButton.addEventListener('click', () => {
        modal.classList.add('save-modal-hidden');
        modal.classList.remove('save-modal-visible');
    });

    
    // Save post to board function
    boardButtons.forEach(button => {
        button.addEventListener('click', () => {
            const boardId = button.getAttribute('data-board-id');
            const postId = saveButton.getAttribute('data-post-id');

            fetch(`/profile/save-to-board/${postId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken, // Ensure the CSRF token is included
                },
                body: `board_id=${boardId}`,
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                        modal.classList.add('save-modal-hidden');
                    } else {
                        alert(data.message || 'An error occurred.');
                    }
                })
                .catch(error => console.error('Error saving post:', error));
        });
    });


    const saveModal = document.getElementById('save-to-board-modal');
    const createModal = document.getElementById('create-board-modal');
    const openCreateBoardBtn = document.getElementById('open-create-board-modal');
    const cancelCreateBoardBtn = document.getElementById('cancel-create-board');
    const submitCreateBoardBtn = document.getElementById('submit-create-board');
    const boardTitleInput = document.getElementById('board-title-input');
    const postImagePreview = document.getElementById('post-image-preview');
    const errorMessage = document.getElementById('board-error-message');

    const popUpMessageOverlay = document.querySelector('.pop-up-message-overlay');
    const popUpMessageContent = document.querySelector('.pop-up-message-content')
    const popUpMessageText = document.querySelector('.pop-up-message-text');

    /**
     * Display a pop-up message.
     * @param {string} message - The message to display.
     */
    function showPopUpMessage(message) {
        popUpMessageText.textContent = message;
        popUpMessageContent.classList.add('pop-up-show-modal')

        //Hide the message after 2 seconds
        setTimeout(() => {
            popUpMessageContent.classList.remove('pop-up-show-modal')

            // Clear the message after the animation
            setTimeout(() => {
                popUpMessageText.textContent = '';
            }, 500); // Match the CSS transition duration
        }, 2000);
    }

    // Open Create Board Modal
    openCreateBoardBtn.addEventListener('click', () => {
        saveModal.classList.add('save-modal-hidden');
        createModal.classList.remove('create-modal-hidden');
        errorMessage.style.display = 'none';
        errorMessage.textContent = '';
    });

    // Close Create Board Modal
    cancelCreateBoardBtn.addEventListener('click', () => {
        createModal.classList.add('create-modal-hidden');
        errorMessage.style.display = 'none';
        errorMessage.textContent = '';
    });

    // Submit Create Board
    submitCreateBoardBtn.addEventListener('click', () => {
        const boardTitle = boardTitleInput.value.trim();
        if (!boardTitle) {
            showPopUpMessage('Please enter a board title.');
            return;
        }

        const postId = postImagePreview.getAttribute('data-post-id'); // Pass the post ID dynamically

        //errorMessage.style.display = 'none';
        //errorMessage.textContent = '';

        fetch('/profile/create-board/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
            },
            body: `title=${encodeURIComponent(boardTitle)}&post_id=${postId}`,
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errData => {
                        throw new Error(errData.error || 'Failed to create board.');
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    showPopUpMessage(data.message);
                    createModal.classList.add('create-modal-hidden');
                    boardTitleInput.value = '';
                } else {
                    showPopUpMessage(data.error || 'An error occurred.');
                }
            })
            .catch(error => {
                showPopUpMessage(error.message || 'An unexpected error occurred. Please try again.');
            });
    });

    // Variables specific to the delete post modal
    const deletePostBtn = document.getElementById('delete-post-btn');
    const deletePostModal = document.getElementById('delete-post-modal');
    const cancelDeletePostBtn = document.getElementById('cancel-delete-post-btn');

    // Open the delete post modal
    if (deletePostBtn) {
        deletePostBtn.addEventListener('click', () => {
            deletePostModal.classList.remove('hidden');
            deletePostModal.classList.add('delete-post-modal-visible')
        });
    }

    // Close the delete post modal
    if (cancelDeletePostBtn) {
        cancelDeletePostBtn.addEventListener('click', () => {
            deletePostModal.classList.add('hidden');
            deletePostModal.classList.remove('delete-post-modal-visible')
        });
    }
});