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


//Loads preview of selected image on PostForm
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


// Image Tags Search Scripts
document.addEventListener('DOMContentLoaded', function() {
    let currentRequest = null;

    const tagInput = document.getElementById('tag-input');
    const suggestionsBox = document.getElementById('tag-suggestions');
    const selectedTagsContainer = document.getElementById('selected-tags');
    const hiddenTagsField = document.getElementById('id_tags');

    let selectedTags = []; // store {id, tag_name} of chosen tags

    // Update hidden field whenever selectedTags changes
    function updateHiddenField() {
        const ids = selectedTags.map(t => t.id);
        // Set the hidden select field to these ids
        // If form.tags is a MultipleHiddenInput, you can just set value as a comma-separated list or
        // dynamically create option elements. 
        // For MultipleHiddenInput, just set it as a comma-separated string:
        hiddenTagsField.value = ids.join(',');
    }

    // Render the selected tags in the UI
    function renderSelectedTags() {
        selectedTagsContainer.innerHTML = '';
        selectedTags.forEach(tag => {
            const tagEl = document.createElement('span');
            tagEl.classList.add('tag');
            tagEl.textContent = tag.tag_name;

            const removeEl = document.createElement('span');
            removeEl.classList.add('remove-tag');
            removeEl.textContent = 'x';
            removeEl.addEventListener('click', function() {
                // Remove this tag from selectedTags
                selectedTags = selectedTags.filter(t => t.id !== tag.id);
                renderSelectedTags();
                updateHiddenField();
            });

            tagEl.appendChild(removeEl);
            selectedTagsContainer.appendChild(tagEl);
        });
    }

    // Fetch suggestions from the server
    function fetchSuggestions(query) {
        if (currentRequest) {
            currentRequest.abort(); // Abort previous request if still ongoing
        }
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '/tag-suggestions/?q=' + encodeURIComponent(query), true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText);
                console.log('Data returned from server:', data);
                showSuggestions(data);
            }
            currentRequest = null;
        };

        xhr.onerror = function() {
            currentRequest = null;
        };

        xhr.send();
        currentRequest = xhr;
    }

    function showSuggestions(tags) {
        suggestionsBox.innerHTML = '';
        if (tags.length > 0 && selectedTags.length < 3) {
            tags.forEach(tag => {
                // Only show tags not already selected
                if (!selectedTags.find(t => t.id === tag.id)) {
                    const div = document.createElement('div');
                    div.textContent = tag.tag_name;
                    div.addEventListener('click', function() {
                        // Add this tag to selectedTags if less than 3
                        if (selectedTags.length < 3) {
                            selectedTags.push(tag);
                            renderSelectedTags();
                            updateHiddenField();
                            suggestionsBox.style.display = 'none';
                            tagInput.value = ''; // clear input after selection
                        }
                    });
                    suggestionsBox.appendChild(div);
                }
            });
            // If after filtering all selected tags out, no new tags remain, show a message.
            if (suggestionsBox.childNodes.length > 0) {
                suggestionsBox.style.display = 'block';
            } else {
                suggestionsBox.innerHTML = '<div>No new tags found</div>';
                suggestionsBox.style.display = 'block';
            }
        } else {
            // If no matches found at all
            suggestionsBox.innerHTML = '<div>No tags found</div>';
            suggestionsBox.style.display = 'block';
    }
}

    // Handle input events on tagInput
    tagInput.addEventListener('input', function() {
        const query = tagInput.value.trim();
        if (query.length > 0 && selectedTags.length < 3) {
            fetchSuggestions(query);
        } else {
            suggestionsBox.style.display = 'none';
        }
    });

    // Hide suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!document.getElementById('tag-autocomplete-container').contains(e.target)) {
            suggestionsBox.style.display = 'none';
        }
    });
});