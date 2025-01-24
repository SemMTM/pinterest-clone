document.addEventListener('DOMContentLoaded', () => {
    const authModal = document.getElementById('auth-modal');
    const authModalContent = document.getElementById('auth-modal-content');
    const loginLink = document.getElementById('login-link');
    const signupLink = document.getElementById('signup-link');
    const closeAuthModal = document.getElementById('close-auth-modal');

    // Open the modal and load content dynamically
    const openAuthModal = async (url) => {
        try {
            const response = await fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
            });
            const data = await response.json();
            authModalContent.innerHTML = data.html;
            authModal.classList.remove('hidden');
        } catch (error) {
            console.error('Error loading modal content:', error);
        }
    };

    // Close the modal
    const closeModal = () => {
        authModal.classList.add('hidden');
        authModalContent.innerHTML = '';
    };

    // Event listeners
    if (loginLink) {
        loginLink.addEventListener('click', (e) => {
            e.preventDefault();
            openAuthModal(loginLink.href);
        });
    }

    if (signupLink) {
        signupLink.addEventListener('click', (e) => {
            e.preventDefault();
            openAuthModal(signupLink.href);
        });
    }

    if (closeAuthModal) {
        closeAuthModal.addEventListener('click', closeModal);
    }

    // Close modal on clicking outside the content
    authModal.addEventListener('click', (e) => {
        if (e.target === authModal) closeModal();
    });

    authModalContent.addEventListener('submit', async (e) => {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
    
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                body: formData,
            });
    
            if (response.ok) {
                // Handle successful login/signup
                window.location.reload(); // Or redirect to another page
            } else {
                const data = await response.json();
                authModalContent.innerHTML = data.html; // Reload the form with errors
            }
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    });
});