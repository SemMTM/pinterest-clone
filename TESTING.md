# **Testing**
## **Integration Testing**

| **Test #** | **User Story** | **Description** | **Steps** | **Expected Outcome** | **Actual Outcome** | **Result** |
|--|--|--|--|--|--|--|
| **Home Page** |  |  |  |  |  |  |
| TC001 |  | Post list returns all posts |  |  |  |  |
| TC002 |  | Masonry grid loads images from left to right |  |  |  |  |
| TC003 |  | Masonry grid calculates image dimensions and adjusts layout to compensate |  |  |  |  |
| TC004 |  | Images are paginated as you scroll |  |  |  |  |
| TC005 |  | Masonry grid adjusts for newly paginated images after pagination |  |  |  |  |
| **Post Upload** |  |  |  |  |  |  |
| TC006 |  | Login modal opened if non-authenticated user tries to open post upload page |  |  |  |  |
| TC007 |  | Images can be uploaded to the webiste |  |  |  |  |
| TC008 |  | Can't upload a post without a title |  |  |  |  |
| TC009 |  | Can't upload a post without an image |  |  |  |  |
| TC010 |  | Can't upload an image that exceeds max file size |  |  |  |  |
| TC011 |  | Post title cannot be over character limit |  |  |  |  |
| TC012 |  | Post description cannot be over character limit |  |  |  |  |
| TC013 |  | Preview of image to be uploaded shown after image is selected |  |  |  |  |
| TC014 |  | Tag suggestions are shown as user types each letter |  |  |  |  |
| TC015 |  | Login modal opened if non-authenticated user tries to open post upload page |  |  |  |  |
| TC016 |  | Tags appear on form after selection |  |  |  |  |
| TC017 |  | 3 tags can be selected at maximum |  |  |  |  |
| TC018 |  | Tags appear on post detail page after selection and upload |  |  |  |  |
| TC019 |  | Title appears on image after upload |  |  |  |  |
| TC020 |  | Description appears on image after upload |  |  |  |  |
| TC021 |  | Login modal opened if non-authenticated user tries to open post upload page |  |  |  |  |
| TC022 |  | Unauthenticated users are taken to a login page of they try to access the image upload page via URL |  |  |  |  |
| TC023 |  | Only alloed file types can be uploaded as posts |  |  |  |  |
| **Profile Page** |  |  |  |  |  |  |
| TC024 |  | Profile is auto-created for user on sign-up |  |  |  |  |
| TC025 |  | 'All Pin' board is auto-created for user on sign up  |  |  |  |  |
| TC026 |  | 'Log-out', 'Edit Profile', 'Created' and 'Saved' button all appear on the profile page for the profile owner |  |  |  |  |
| TC027 |  | 'Created' section shows all of the users uploaded posts |  |  |  |  |
| TC028 |  | New boards appear in the 'Saved' section after creation |  |  |  |  |
| TC029 |  | Profile page log out button logs the user out |  |  |  |  |
| TC030 |  | 'Edit Profile' button opens the edit profile modal |  |  |  |  |
| TC031 |  | Submitted changes in the edit profile modal are publicly displayed on the users profile page |  |  |  |  |
| TC032 |  | Other users can see a users profile and their public information |  |  |  |  |
| TC033 |  | 'Created' sections pagination works on page scroll |  |  |  |  |
| TC034 |  | Profile image is displayed in all relevant places after upload |  |  |  |  |
| TC035 |  | Can't exceed character limits on edit profile modal inputs |  |  |  |  |
| TC036 |  | Can't upload a profile image that exceeds the maximum file size |  |  |  |  |
| TC037 |  | Can only upload allowed file types as profile image |  |  |  |  |
| TC038 |  | Profile image preview is displayed after image is selected |  |  |  |  |
| TC039 |  | Newly created profiles have a default profile image |  |  |  |  |
| TC040 |  | Image boards show the number of posts saved to it |  |  |  |  |
| TC041 |  | Image boards preview images are shown from images pinned to the board |  |  |  |  |
| TC042 |  | When edit profile changes are submitted, the profile page is updated dynamically |  |  |  |  |
| TC043 |  | Profile page button on nav bar only accessible for logged in users |  |  |  |  |
| TC044 |  | A non-existant profile cannot be accessed by URL |  |  |  |  |
| TC045 |  | 'All Pins' board only accessible by the profile owner |  |  |  |  |
| TC046 |  | Boards set to private are only visisble and accessible by the board owner |  |  |  |  |
| TC047 |  | You can navigate to a users profile via URL (case-insensetive) |  |  |  |  |
| **Board Detail Page** |  |  |  |  |  |  |
| TC048 |  | Boards can be opened to view pinned posts |  |  |  |  |
| TC049 |  | Masonry grid works as expected on board detail page |  |  |  |  |
| TC050 |  | Edit board button only appears for board owner |  |  |  |  |
| TC051 |  | Only board owner can edit a board |  |  |  |  |
| TC052 |  | Unpin button only appears for board owner |  |  |  |  |
| TC053 |  | Unpinned image is removed from board |  |  |  |  |
| TC054 |  | 'All Pins' board cannot be edited by any user |  |  |  |  |
| TC055 |  | Edit board button not visisble on 'All Pins' board for any user |  |  |  |  |
| TC056 |  | Deleteing a board removed it from a users profile page |  |  |  |  |
| TC057 |  | A deleted board cannot be accessed by URL |  |  |  |  |
| TC058 |  | A private board can only be seen by the board owner |  |  |  |  |
| TC059 |  | A user cannot access a private board by URL |  |  |  |  |
| TC060 |  | Board title changes can be seen by all users |  |  |  |  |
| TC061 |  | After a board title is changed, it is updated dynamically |  |  |  |  |
| TC062 |  | An unpinned image is dyanmically removed from a board |  |  |  |  |
| TC063 |  | A newly saved image is displayed in the correct board |  |  |  |  |
| TC064 |  | An image saved to anyboard is automatically added to the 'All Pins' board |  |  |  |  |
| TC065 |  | The correct posts are displated when clicking into a board |  |  |  |  |
| **Post Detail Page** |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
| **Authentication** |  |  |  |  |  |  |
|  |  |  |  |  |  |  |