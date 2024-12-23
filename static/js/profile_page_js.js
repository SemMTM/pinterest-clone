document.addEventListener('DOMContentLoaded', () => {
    const createdButton = document.getElementById('created-btn');
    const createdContainer = document.getElementById('created-container');
    const savedContainer = document.getElementById('saved-container');
    const savedButton = document.getElementById('saved-btn');

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
});