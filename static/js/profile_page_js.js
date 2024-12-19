document.addEventListener('DOMContentLoaded', () => {
    // Load created posts script
    const createdButton = document.getElementById('created-btn');
    const createdContainer = document.getElementById('created-container');
    const username = createdContainer.dataset.username; // Fetch the username from the data attribute

    createdButton.addEventListener('click', async () => {
        try {
            const fetchUrl = `/profile/${username}/created/`; // Construct the URL using the username
            console.log(`Fetching from URL: ${fetchUrl}`);

            const response = await fetch(fetchUrl);
            if (!response.ok) {
                console.error(`HTTP Error: ${response.status} ${response.statusText}`);
                throw new Error(`Failed to load created pins. Status: ${response.status}`);
            }

            const html = await response.text();
            createdContainer.innerHTML = html; // Inject the fetched HTML into the container
            console.log('Created posts loaded successfully.');
        } catch (error) {
            console.error('Error loading created posts:', error);
            alert('Error loading created posts. Please try again later.');
        }
    });
});