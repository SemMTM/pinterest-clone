document.addEventListener('DOMContentLoaded', function() {
    // Save modal scripts
    const saveButton = document.getElementById('save-btn');
    const modal = document.getElementById('save-to-board-modal');
    const closeModalButton = document.getElementById('close-save-modal');
    const boardButtons = document.querySelectorAll('.save-modal-board-btn');
    const isAuthenticated = saveButton.getAttribute('data-authenticated');

    // Open modal
    saveButton.addEventListener('click', () => {
        if (!isAuthenticated) {
            alert("Log in to save posts");
        } else {
            modal.classList.remove('save-modal-hidden');
        }
    });

    // Close modal
    closeModalButton.addEventListener('click', () => {
        modal.classList.add('save-modal-hidden');
    });

    
    // Handle board selection
    boardButtons.forEach(button => {
        button.addEventListener('click', () => {
            const boardId = button.getAttribute('data-board-id');
            const postId = saveButton.getAttribute('data-post-id');

            fetch(`/profile/save-to-board/${postId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'), // Ensure the CSRF token is included
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


    const saveModal = document.getElementById('save-to-board-modal');
    const createModal = document.getElementById('create-board-modal');
    const openCreateBoardBtn = document.getElementById('open-create-board-modal');
    const cancelCreateBoardBtn = document.getElementById('cancel-create-board');
    const submitCreateBoardBtn = document.getElementById('submit-create-board');
    const boardTitleInput = document.getElementById('board-title-input');
    const postImagePreview = document.getElementById('post-image-preview');
    const errorMessage = document.getElementById('board-error-message');

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
            errorMessage.textContent = 'Please enter a board title.';
            errorMessage.style.display = 'block';
            return;
        }

        const postId = postImagePreview.getAttribute('data-post-id'); // Pass the post ID dynamically

        errorMessage.style.display = 'none';
        errorMessage.textContent = '';

        fetch('/profile/create-board/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken'),
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
                    alert(data.message);
                    createModal.classList.add('create-modal-hidden');
                    boardTitleInput.value = '';
                } else {
                    errorMessage.textContent = data.error || 'An error occurred.';
                    errorMessage.style.display = 'block';
                }
            })
            .catch(error => {
                errorMessage.textContent = error.message || 'An unexpected error occurred. Please try again.';
                errorMessage.style.display = 'block';
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
        });
    }

    // Close the delete post modal
    if (cancelDeletePostBtn) {
        cancelDeletePostBtn.addEventListener('click', () => {
            deletePostModal.classList.add('hidden');
        });
    }
});