const backButton = document.getElementById('back-button');

if (backButton) {
    backButton.addEventListener('click', function (e) {
        if (document.referrer) {
            // Prevent default link behavior and navigate to referrer
            e.preventDefault();
            window.location.href = document.referrer;
        } else {
            // Allow the default link behavior (fallback to href)
        }
    });
}
