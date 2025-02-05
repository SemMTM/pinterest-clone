const popUpMessageContent = document.querySelector('.pop-up-message-content')
const popUpMessageText = document.querySelector('.pop-up-message-text');

/**
     * Display a pop-up message.
     * @param {string} message - The message to display.
     */
export function showPopUpMessage(message) {
    popUpMessageText.textContent = message;
    popUpMessageContent.classList.add('pop-up-show-modal')

    //Hide the message after 2 seconds
    setTimeout(() => {
        popUpMessageContent.classList.remove('pop-up-show-modal')

        // Clear the message after the animation
        setTimeout(() => {
            popUpMessageText.textContent = '';
        }, 2500); // Match the CSS transition duration
    }, 2500);
}