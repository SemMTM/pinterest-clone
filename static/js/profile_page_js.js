document.addEventListener('DOMContentLoaded', () => {
    // Load created posts script
    const createdButton = document.getElementById('created-btn');
    const createdContainer = document.getElementById('created-container');
    const savedContainer = document.getElementById('saved-container');
    const username = createdContainer.dataset.username; // Fetch the username from the data attribute

    //createdButton.addEventListener('click', async () => {
        //createdButton.disabled = true;
        //try {
        //    const fetchUrl = `/profile/${username}/created/`; // Construct the URL using the username
        //    const response = await fetch(fetchUrl);
        //    if (!response.ok) {
        //        throw new Error(`Failed to load created pins. Status: ${response.status}`);
        //    }
        //    const html = await response.text();
        //    createdContainer.innerHTML = html; // Inject the fetched HTML into the container;
        //} catch (error) {
        //    console.error('Error loading created posts:', error);
        //    alert('Error loading created posts. Please try again later.');
        //} finally {
        //    createdButton.disabled = false; 
        //}
    //});

    const savedButton = document.getElementById('saved-btn');

    const toggleActive = (buttonToActivate, buttonToDeactivate) => {
        buttonToActivate.classList.add('active');
        buttonToDeactivate.classList.remove('active');
    };

    const toggleHidden = (addHidden, removeHidden) => {
        addHidden.classList.add('hidden');
        removeHidden.classList.remove('hidden');
    };

    createdButton.addEventListener('click', () => {
        toggleActive(createdButton, savedButton);
        toggleHidden(savedContainer, createdContainer);
    });
    savedButton.addEventListener('click', () => {
        toggleActive(savedButton, createdButton);
        toggleHidden(createdContainer, savedContainer);

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