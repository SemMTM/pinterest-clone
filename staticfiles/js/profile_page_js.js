import { showPopUpMessage } from './pop_up.js'

document.addEventListener('DOMContentLoaded', () => {
    const createdButton = document.getElementById('created-btn');
    const createdContainer = document.getElementById('created-container');
    const savedContainer = document.getElementById('saved-container');
    const savedButton = document.getElementById('saved-btn');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    // Helper functions for toggling active and pointer events
    const toggleActive = (buttonToActivate, buttonToDeactivate) => {
        buttonToActivate.classList.add('active');
        buttonToDeactivate.classList.remove('active');

        if (buttonToDeactivate != createdButton) {
            createdButton.style.pointerEvents = 'none';
            createdButton.style.cursor = 'not-allowed';
        } else {
            createdButton.style.pointerEvents = '';
            createdButton.style.cursor = '';
        }
    }; 

    const toggleHidden = (addHidden, removeHidden) => {
        addHidden.classList.add('hidden');
        removeHidden.classList.remove('hidden');
    };

    createdButton.addEventListener('click', () => {
        toggleActive(createdButton, savedButton);
        toggleHidden(savedContainer, createdContainer);
        createdContainer.classList.add('image-grid');
    });
    savedButton.addEventListener('click', () => {
        toggleActive(savedButton, createdButton);
        toggleHidden(createdContainer, savedContainer);
        createdContainer.classList.remove('image-grid');
    });

    const editBoardButton = document.getElementById('edit-board-btn');
    
    if (editBoardButton) {
        editBoardButton.addEventListener('click', (e) => {
            e.preventDefault();
            const modal = document.getElementById('edit-board-modal');
            modal.classList.remove('hidden'); // Show the modal
        });
    }

    // Handle Edit Profile Modal
    const editProfileButton = document.getElementById('edit-profile-btn'); 
    const editProfileModal = document.getElementById('edit-profile-modal');
    const editProfileModalContent = document.getElementById('edit-profile-modal-content')
    const cancelEditProfileButton = document.getElementById('cancel-edit-profile-btn');

    const showModal = () => {
        editProfileModal.classList.add('modal-show');
        editProfileModalContent.classList.add('edit-profile-modal-visible');
    }

    const hideModal = () => { 
        editProfileModal.classList.remove('modal-show'); 
        editProfileModalContent.classList.remove('edit-profile-modal-visible');
    }
    
    editProfileButton.addEventListener('click', showModal);

    cancelEditProfileButton.addEventListener('click', hideModal)

    // ----- Client-Side Validation for edit profile form -----
    const imagePreview = document.getElementById('profile-image-preview');
    const profileImageInput = document.getElementById('profile_image');
    const max_file_size = 20 * 1024 * 1024;

    profileImageInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
    
        if (file) {
            const fileSize = file.size; // Get file size in bytes
            const allowedExtensions = ['jpg', 'jpeg', 'png', 'webp'];
            const fileExtension = file.name.split('.').pop().toLowerCase();

            // Validate file type
            if (!allowedExtensions.includes(fileExtension)) {
                    showPopUpMessage('Only JPG, JPEG, PNG, and WEBP files are allowed.');
                    this.value = ''; // Reset the input
                    return;
                }
    
            // Validate file size
            if (fileSize > max_file_size) {
                showPopUpMessage('The uploaded image exceeds the maximum file size of 20MB.');
                this.value = ''; // Reset the input
                return;
            }
            
            // If file is valid, show preview
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    const editProfileForm = document.getElementById('edit-profile-form');

    // Submit on enter
    if (editProfileForm) {
        editProfileForm.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) { // Prevents new line on Enter + Shift
                event.preventDefault(); // Prevents default newline behavior
                editProfileForm?.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
            }
        });
    }

    // Edit profile form submission and dynamic update
    if (editProfileForm) {
        editProfileForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(editProfileForm);
            const url = editProfileForm.getAttribute('action');

            fetch(url, {
                method: 'POST', 
                headers: {
                    'X-CSRFToken': csrfToken,
                },
                body: formData,
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Failed to update profile.');
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.success) {
                        // Update profile information dynamically
                        const profileUserIcon = document.getElementById('profile-user-icon');
                        if (profileUserIcon) {
                            profileUserIcon.style.backgroundImage = `url(${data.data.profile_image})`;
                            profileUserIcon.style.backgroundSize = 'cover';
                            profileUserIcon.style.backgroundPosition = 'center';
                        }

                        const usernameElement = document.getElementById('user-full-name');
                        if (usernameElement) {
                            usernameElement.textContent = `${data.data.first_name} ${data.data.last_name}`.trim() || usernameElement.textContent;
                        }

                        const userAboutElement = document.getElementById('pp-about');
                        if(userAboutElement) {
                            userAboutElement.textContent = `${data.data.about}`.trim() || userAboutElement.textContent;
                        }
                        showPopUpMessage(data.message);
                    } else {
                        showPopUpMessage(data.error || 'An error occurred.');
                    }
                })
                .catch((error) => showPopUpMessage(error.message || 'An unexpected error occurred. Please try again.'));
            hideModal();
        });
    }
});