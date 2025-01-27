document.addEventListener('DOMContentLoaded', () => {
    const authModal = document.getElementById('auth-modal');
    const authModalContent = document.getElementById('auth-modal-content');
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

    // Attach event listeners to all login/signup links
    const attachModalListeners = () => {
        const authLinks = document.querySelectorAll(
            'a[href$="/custom-accounts/login-modal/"], a[href$="/custom-accounts/signup-modal/"]'
        );

        authLinks.forEach((link) => {
            link.addEventListener('click', (e) => {
                e.preventDefault(); // Prevent default navigation
                const url = link.getAttribute('href');
                openAuthModal(url); // Open the modal with the corresponding content
            });
        });
    };

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

    // Attach modal listeners to links dynamically on page load
    attachModalListeners();

    // Reattach modal listeners after dynamic content is loaded (if using htmx or similar)
    document.body.addEventListener('htmx:afterSwap', attachModalListeners);
});