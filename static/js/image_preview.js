// Client side validation  for file type on PostForm image 
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('id_image');
    fileInput.addEventListener('change', function() {
        const file = this.files[0]; // Retrieves the first file selected by the user.
        if (file) {
            const allowedExtensions = ['jpg', 'jpeg', 'png'];
            const fileExtension = file.name.split('.').pop().toLowerCase();
            // Extracts the file extension by splitting the filename on "." and taking the last segment, then
            // converts it to lowercase

            if (!allowedExtensions.includes(fileExtension)) {
                alert('Only JPG/JPEG/PNG files are allowed.');
                this.value = ''; // Reset the input
            }
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('id_image');
    const preview = document.getElementById('image-preview');

    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();
            // Creates a new FileReader object, which can read the contents of a file
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