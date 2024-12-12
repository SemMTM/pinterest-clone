/* Script for image upload preview */
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('id_image'); // Assuming your form's image field has the ID 'id_image'
    const preview = document.getElementById('image-preview');

    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result; // Set image source to file contents
                preview.style.display = 'block'; // Show the preview image
            };
            reader.readAsDataURL(file); // Read the selected file as a data URL
        } else {
            // If no file is selected, hide the preview
            preview.style.display = 'none';
            preview.src = '';
        }
    });
});

console.log('Script loaded')