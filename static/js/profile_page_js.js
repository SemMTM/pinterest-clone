document.addEventListener('DOMContentLoaded', () => {
    const createdButton = document.getElementById('created-btn'); 
    const contentContainer = document.getElementById('created-container'); 
    const user = createdContainer.dataset.user;

    createdButton.addEventListener('click', async () => {
        try {
            const response = await fetch(`/${user}/created`);
            if (!response.ok) throw new Error('Failed to load created pins.');
            const html = await response.text();

            // Replace the container's content with fetched HTML
            contentContainer.innerHTML = html;
        } catch (error) {
            console.error(error);
            alert('Error loading created posts.');
        }
    });
});