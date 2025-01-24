document.addEventListener('DOMContentLoaded', () => {
    const authModal = document.getElementById('auth-modal');
    const authModalContent = document.getElementById('auth-modal-content');
    const loginLink = document.getElementById('login-link');
    const signupLink = document.getElementById('signup-link');
    const closeAuthModal = document.getElementById('close-auth-modal');

    // Function to open the modal and load content dynamically
    const openAuthModal = async (url) => {
        try {
            const response = await fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }, // AJAX header
            });
            const data = await response.json();
            authModalContent.innerHTML = data.html;
            authModal.classList.remove('hidden');
        } catch (error) {
            console.error('Error loading modal content:', error);
        }
    };

    // Function to close the modal
    const closeModal = () => {
        authModal.classList.add('hidden'); // Hide the modal
        authModalContent.innerHTML = ''; // Clear the modal content
    };

    // Add event listeners for login and signup buttons
    if (loginLink) {
        loginLink.addEventListener('click', (e) => {
            try {
                e.preventDefault(); // Prevent default navigation
                openAuthModal(loginLink.getAttribute('href'));
            } catch (error) {
                console.error('Error opening modal, redirecting:', error);
                window.location.href = loginLink.getAttribute('href'); // Fallback to dedicated page
            }
        });
    }

    if (signupLink) {
        signupLink.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent default navigation
            openAuthModal(signupLink.getAttribute('href')); // Open signup modal
        });
    }

    // Close the modal when the close button is clicked
    if (closeAuthModal) {
        closeAuthModal.addEventListener('click', closeModal);
    }

    // Close the modal when clicking outside the modal content
    authModal.addEventListener('click', (e) => {
        if (e.target === authModal) {
            closeModal();
        }
    });

    // Handle form submission within the modal
    authModalContent.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission
        const form = e.target;
        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                body: formData,
            });

            if (response.ok) {
                window.location.reload(); // Reload the page on successful login/signup
            } else {
                const data = await response.json();
                authModalContent.innerHTML = data.html; // Reload the modal with error messages
            }
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    });
});