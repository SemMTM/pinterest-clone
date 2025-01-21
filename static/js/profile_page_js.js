import { showPopUpMessage } from './pop_up.js'

document.addEventListener('DOMContentLoaded', () => {
    const createdButton = document.getElementById('created-btn');
    const createdContainer = document.getElementById('created-container');
    const savedContainer = document.getElementById('saved-container');
    const savedButton = document.getElementById('saved-btn');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    const toggleActive = (buttonToActivate, buttonToDeactivate) => {
        buttonToActivate.classList.add('active');
        buttonToDeactivate.classList.remove('active');

        if (buttonToDeactivate != createdButton) {
            createdButton.style.pointerEvents = 'none';
            createdButton.style.cursor = 'not-allowed';
        } else {
            createdButton.style.pointerEvents = '';
            createdButton.style.cursor = ''; // Reactivate the saved button when it's not active
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
    const editProfileForm = document.getElementById('edit-profile-form');
    const profileImageInput = document.getElementById('profile_image');
    const imagePreview = document.getElementById('profile-image-preview');

    const showModal = () => {
        editProfileModal.classList.remove('hidden');
        editProfileModalContent.classList.add('edit-profile-modal-visible');
    }

    const hideModal = () => {
        editProfileModal.classList.add('hidden'); 
        editProfileModalContent.classList.remove('edit-profile-modal-visible');
    }
    
    editProfileButton.addEventListener('click', showModal);

    cancelEditProfileButton.addEventListener('click', hideModal)

    // Image Preview on profile edit modal
    profileImageInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result; // Update the preview image source
            };
            reader.readAsDataURL(file);
        }
    });

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

                        editProfileModal.classList.add('hidden'); // Hide modal
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