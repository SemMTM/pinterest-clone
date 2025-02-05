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
| TC096 |  | Image tags can be deleted |  |  |  |  |
| TC097 |  | Post form is cleared after image is uploaded |  |  |  |  |
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
| TC066 |  | The correct image is opened on post click |  |  |  |  |
| TC067 |  | A logged in user can like a post |  |  |  |  |
| TC068 |  | The number of likes a post has can be seen by all users |  |  |  |  |
| TC069 |  | After clicking on a post uploaders profile, you are taken to their profile page |  |  |  |  |
| TC070 |  | A user can remove their like from a post |  |  |  |  |
| TC071 |  | A user can delete their own post |  |  |  |  |
| TC072 |  | Any logged in user can comment on a post |  |  |  |  |
| TC073 |  | Comments on a post can be seen by all users |  |  |  |  |
| TC074 |  | The post owner can delete any comments on their posts |  |  |  |  |
| TC075 |  | You can see the amount of time ago a comment was made |  |  |  |  |
| TC076 |  | The total number of comments on a post can be seen |  |  |  |  |
| TC077 |  | A user can delete their own comment |  |  |  |  |
| TC078 |  | A user can edit their own comment |  |  |  |  |
| TC079 |  | Comment edit can be seen by other users after publishing |  |  |  |  |
| TC080 |  | The edit comment button is only displayed for the comment creator  |  |  |  |  |
| TC081 |  | The delete comment button is only displayed for the post owner or the commeter |  |  |  |  |
| TC082 |  | The delete post button is only visisble for the post owner |  |  |  |  |
| TC083 |  | A user can save a post to a board |  |  |  |  |
| TC084 |  | A user can create a new board from the save post modal |  |  |  |  |
| **Authentication** |  |  |  |  |  |  |
| TC085 |  | Clicking the logout button, logs a user out |  |  |  |  |
| TC086 |  | When registering, usernames must be unique |  |  |  |  |
| TC087 |  | Usernames cannot have URL unsafe characters |  |  |  |  |
| TC088 |  | A user must validate their password correctly to create an account |  |  |  |  |
| TC089 |  | After account creation a user can sign in with their credentials |  |  |  |  |
| TC090 |  | A user can change their password |  |  |  |  |
| TC091 |  | When creating an account, usernames cannot be blank |  |  |  |  |
| TC092 |  | A user must be logged in to access the post upload page |  |  |  |  |
| TC093 |  | A user must be logged in to comment |  |  |  |  |
| TC094 |  | A user must be logged in to save a post/create a board |  |  |  |  |
| TC095 |  | The sign-up/log-in page is a pop-up modal |  |  |  |  |