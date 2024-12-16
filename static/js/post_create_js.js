document.addEventListener('DOMContentLoaded', function() {
    // ----- Client-Side Validation for File Type on PostForm image -----
    const fileInput = document.getElementById('id_image');
    const preview = document.getElementById('image-preview');

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const allowedExtensions = ['jpg', 'jpeg', 'png'];
                const fileExtension = file.name.split('.').pop().toLowerCase();
                // Extract the file extension and convert it to lowercase for comparison.

                if (!allowedExtensions.includes(fileExtension)) {
                    alert('Only JPG/JPEG/PNG files are allowed.');
                    this.value = ''; // Reset the input
                }
            }
        });

        // Loads preview of selected image on PostForm
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader(); // A FileReader allows reading file contents.
                reader.onload = function(e) {
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            } else if (preview) {
                // If no file is selected, hide the preview
                preview.style.display = 'none';
                preview.src = '';
            }
        });
    }

    // ----- Image Tags Search Scripts -----
    const tagInput = document.getElementById('tag-input');
    const suggestionsBox = document.getElementById('tag-suggestions');
    const selectedTagsContainer = document.getElementById('selected-tags');
    const hiddenTagsContainer = document.getElementById('hidden_tags');

    let selectedTags = [];
    let currentRequest = null;

    function updateHiddenField() {
        if (hiddenTagsContainer) {
            hiddenTagsContainer.innerHTML = '';
            selectedTags.forEach(tag => {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'tags';
                input.value = tag.id;
                hiddenTagsContainer.appendChild(input);
            });
        }
    }

    function renderSelectedTags() {
        // Updates the UI to show which tags have been selected.
        if (!selectedTagsContainer) return;
        selectedTagsContainer.innerHTML = '';
        selectedTags.forEach(tag => {
            const tagEl = document.createElement('span');
            tagEl.classList.add('tag');
            tagEl.textContent = tag.tag_name;

            const removeEl = document.createElement('span');
            removeEl.classList.add('remove-tag');
            removeEl.textContent = 'x';
            removeEl.addEventListener('click', () => {
                // When the 'x' is clicked, remove the corresponding tag from selectedTags.
                selectedTags = selectedTags.filter(t => t.id !== tag.id);
                renderSelectedTags();
                updateHiddenField();
            });

            tagEl.appendChild(removeEl);
            selectedTagsContainer.appendChild(tagEl);
        });
    }

    function showSuggestions(tags) {
        // Displays the suggested tags returned by the server in the dropdown.
        if (!suggestionsBox) return;
        suggestionsBox.innerHTML = '';
        
        if (tags.length > 0 && selectedTags.length < 3) {
            tags.forEach(tag => {
                if (!selectedTags.find(t => t.id === tag.id)) {
                    const div = document.createElement('div');
                    div.textContent = tag.tag_name;
                    div.addEventListener('click', () => {
                        if (selectedTags.length < 3) {
                            selectedTags.push(tag);
                            renderSelectedTags();
                            updateHiddenField();
                            suggestionsBox.style.display = 'none';
                            if (tagInput) tagInput.value = '';
                        }
                    });
                    suggestionsBox.appendChild(div);
                }
            });

            if (suggestionsBox.childNodes.length > 0) {
                suggestionsBox.style.display = 'block';
            } else {
                suggestionsBox.innerHTML = '<div>No new tags found</div>';
                suggestionsBox.style.display = 'block';
            }
        } else {
            suggestionsBox.innerHTML = '<div>No tags found</div>';
            suggestionsBox.style.display = 'block';
        }
    }

    function fetchSuggestions(query) {
        // Performs an AJAX request to fetch matching tags from the server.
        if (currentRequest) currentRequest.abort(); // Abort any previous ongoing request.
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '/tag-suggestions/?q=' + encodeURIComponent(query), true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText); // Parse the server's JSON response.
                showSuggestions(data); // Display the returned suggestions.
            }
            currentRequest = null;
        };
        xhr.onerror = function() { currentRequest = null; };
        xhr.send();
        currentRequest = xhr;
    }

    if (tagInput && suggestionsBox) {
        // Only add event listeners if tag input and suggestions box exist on the page.
        tagInput.addEventListener('input', () => {
            // Whenever the user types in the tag input:
            const query = tagInput.value.trim(); // Trim whitespace around the query.
            if (query.length > 0 && selectedTags.length < 3) {
                fetchSuggestions(query);
            } else {
                suggestionsBox.style.display = 'none';
            }
        });

        document.addEventListener('click', (e) => {
            const container = document.getElementById('tag-autocomplete-container');
            if (container && !container.contains(e.target)) {
                suggestionsBox.style.display = 'none';
            }
        });
    }
});