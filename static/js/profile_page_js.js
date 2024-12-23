document.addEventListener('DOMContentLoaded', () => {
    // Load created posts script
    const createdButton = document.getElementById('created-btn');
    const createdContainer = document.getElementById('created-container');
    const username = createdContainer.dataset.username; // Fetch the username from the data attribute

    createdButton.addEventListener('click', async () => {
        try {
            const fetchUrl = `/profile/${username}/created/`; // Construct the URL using the username
            const response = await fetch(fetchUrl);
            if (!response.ok) {
                console.error(`HTTP Error: ${response.status} ${response.statusText}`);
                throw new Error(`Failed to load created pins. Status: ${response.status}`);
            }

            const html = await response.text();
            createdContainer.innerHTML = html; // Inject the fetched HTML into the container
        } catch (error) {
            console.error('Error loading created posts:', error);
            alert('Error loading created posts. Please try again later.');
        }
    });


    // Boards toggles scripts
    const savedButton = document.getElementById('saved-btn');

    const toggleActive = (buttonToActivate, buttonToDeactivate) => {
        buttonToActivate.classList.add('active');
        buttonToDeactivate.classList.remove('active');
    };

    createdButton.addEventListener('click', () => {
        toggleActive(createdButton, savedButton)
        createdContainer.classList.add('image-grid')
        resizeAllGridItems()
    });
    savedButton.addEventListener('click', () => {
        toggleActive(savedButton, createdButton)
        createdContainer.classList.remove('image-grid')
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