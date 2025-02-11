# **Testing**
## **Integration Testing**

| **Test #** | **User Story** | **Description** | **How we test it** | **Expected Outcome** | **Result** | **Pass/Fail**
|--|--|--|--|--|--|--|
| **Home Page** |  |  |  |  |  |  |
| TC001 | [User Story Link - List of all posts](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87967364&issue=SemMTM%7Cpinterest-clone%7C1) | Post list returns all posts | Navigate to the homepage | All posts displayed on page | As expected | PASS |
| TC002 | [User Story - Masonry grid](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95975414&issue=SemMTM%7Cpinterest-clone%7C22) | Masonry grid loads images from left to right | Navigate to the home page and use devtools to check that the images have been loaded and ordered from left to right | Images have been ordered from left to right in the grid | As expected | PASS |
| TC003 | [User Story - Masonry grid](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95975414&issue=SemMTM%7Cpinterest-clone%7C22) | Masonry grid calculates image dimensions and adjusts layout to compensate | Upload images of different aspect ratios then navigate to the homepage | Images of different aspect ratios fit into the masonry grid with even gaps between them | As expected | PASS |
| TC004 | [User Story Link - List of all posts](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87967364&issue=SemMTM%7Cpinterest-clone%7C1) | Images are paginated as you scroll | Navigate to the homepage then scroll down | More images are loaded on page scroll | As expected | PASS |
| TC005 | [User Story - Masonry grid](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95975414&issue=SemMTM%7Cpinterest-clone%7C22) | Masonry grid adjusts for newly paginated images after pagination | Navigate to the homepage then scroll down | Paginated images are placed within the masonry grid layout | As expected | PASS |
| **Post Upload** |  |  |  |  |  |
| TC006 |  | Login modal opened if non-authenticated user tries to open post upload page | Click on the new post button while logged out | Login modal pops up | As expected | PASS |
| TC007 | [User Story - Image upload](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87986375&issue=SemMTM%7Cpinterest-clone%7C17) | Images can be uploaded to the webiste | Upload an image to the app from the post create page after logging in, then navigate to the homepage and find your uploaded image | Users post has been successfully uploaded | As expected | PASS |
| TC008 |  | Can't upload a post without a title | Log in, navigate to post create page, try to upload an image with no title | Error message displayed and upload prevented | As expected | PASS |
| TC009 |  | Can't upload a post without an image | Log in, navigate to post create page, try to upload an image with no image | Error message displayed and upload prevented | As expected | Pass |
| TC010 |  | Can't upload an image that exceeds max file size | Log in, navigate to post create page, try to upload an image over 20mb | Error message displayed and upload prevented | As expected | PASS |
| TC011 |  | Post title cannot be over character limit | Log in, navigate to post create page, try to add a 101 character title | User cannot type more than 100 characters in the title field | As expected | PASS |
| TC012 |  | Post description cannot be over character limit | Log in, navigate to post create page, try to add a 301 character description | User cannot type more than 300 characters in the description field | As expected | PASS |
| TC013 |  | Preview of image to be uploaded shown after image is selected | Navigate to post create page and select an image to upload | Image preview of selected file shown above file selector | As expected | PASS |
| TC014 |  | Tag suggestions are shown as user types each letter | Navigate to post create page, type the letter c in tag suggestion input | Up to 10 tags shown related to the letter c | As expected | PASS |
| TC015 |  | Image tags can be deleted | Navigate to post create page, select 3 tags then delete them by pressing the x next to the tag | Deleted tags are removed from the selected tags list | As expected | PASS |
| TC016 |  | Tags appear on form after selection | Navigate to post create page, select 3 tags | Selected tags appear above tag input box | As expected | PASS |
| TC017 | [User Story - Image tags](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95978372&issue=SemMTM%7Cpinterest-clone%7C27) | 3 tags can be selected at maximum | Navigate to post create page, select 3 tags then try to add another one | After 3 tags have been selected, no more can be selected | As expected | PASS |
| TC018 | [User Story - Image tags](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95978372&issue=SemMTM%7Cpinterest-clone%7C27) | Tags appear on post detail page after selection and upload | Upload an image with 3 tags then find that post and click on it | Selected tags appear in post detail page | As expected | PASS |
| TC019 | [User Story - Create a post](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87986375&issue=SemMTM%7Cpinterest-clone%7C17) | Title appears on image after upload | Upload an image with a title then find it and click on it | Title visible above image on post detail page | As expected | PASS |
| TC020 | [User Story - Create a post](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87986375&issue=SemMTM%7Cpinterest-clone%7C17) | Description appears on image after upload | Upload a post with a description, find it on the homepage and click on it | Post description visisble on post detail page | As expected | PASS |
| TC021 |  | Post form is cleared after image is uploaded | Upload a post | Post from cleared after upload | As expected | PASS |
| TC022 |  | Unauthenticated users are taken to a login page of they try to access the image upload page via URL | Copy the post create page url, log out, paste the URL into the search bar | User is taken to a login page | Unauthenticated user was taken to post upload page | FAIL |
| TC022 #2 |  | Add @login_required to post_create view and styles for standalone login page not on modal | Re-try TC022 | User is taken to a login page | As expected | PASS |
| TC023 |  | Only allowed file types can be uploaded as posts | Navigate to the post create page, try to upload a PDF file in the image selector | Error message displayed and file not uploaded | As expected | PASS |
| **Profile Page** |  |  |  |  |  |
|  | [User Story - View created image boards](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87981322&issue=SemMTM%7Cpinterest-clone%7C11) | A list of created image boards can be seen on the profile page | Log in, click on a post, click save, create an image board, then navigate to the profile page | A list of image boards including the newly created one are visible | As expected | PASS |
|  | [User Story - Another users image boards](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87982835&issue=SemMTM%7Cpinterest-clone%7C15) | A users image boards are visisble on their profile | Click on a post then click on the uploaders profile | A list of their created image boards are visisble | As expected | PASS |
| TC024 | [User Story - Profile creation](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95979352&issue=SemMTM%7Cpinterest-clone%7C29) | Profile is auto-created for user on sign-up | Create a new user, then navigate to the profile page | Users profile page opens with their username clearly visisble | As expected | PASS |
| TC025 | [User Story - All pins board](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95979980&issue=SemMTM%7Cpinterest-clone%7C30) | 'All Pin' board is auto-created for user on sign up  | Create a new user, then navigate to the profile page | All Pins board can be seen with no pins in it | As expected | PASS |
| TC026 | [User Story - Logout](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95981777&issue=SemMTM%7Cpinterest-clone%7C34) | 'Log-out', 'Edit Profile', 'Created' and 'Saved' button all appear on the profile page for the profile owner | Log in, navigate to the profile page. Log in as a different user, then go to the previous users profile paage | All buttons are visisble for profile owner, only the "saved" and "created" buttons are visisble for the other user | As expected | PASS |
| TC027 | [User Story - View created posts](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87981681&issue=SemMTM%7Cpinterest-clone%7C12) | 'Created' section shows all of the users uploaded posts | Navigate to a users profile page and click the "Created" button | A list of the users uploaded posts are shown | As expected | PASS |
| TC028 | [User Story - Create image boards](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87972960&issue=SemMTM%7Cpinterest-clone%7C10) | New boards appear in the 'Saved' section after creation | Log in, create a new image board, navigate to the profile page | The newly created board can be seen in the list | As expected | PASS |
| TC029 | [User Story - Log out](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95981777&issue=SemMTM%7Cpinterest-clone%7C34) | Profile page log out button logs the user out | Log in, navigate to the profile page, click log out | User is logged out | As expected | PASS |
| TC030 |  | 'Edit Profile' button opens the edit profile modal | Log in, navigate to the profile page, click "Edit Profile" | Edit profile modal pops up | As expected | PASS |
| TC031 | [User Story - Manage profile](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87982051&issue=SemMTM%7Cpinterest-clone%7C13) | Submitted changes in the edit profile modal are publicly displayed on the users profile page | Log in, navigate to the profile page, open the edit profile modal, make changes to first and last name and save them. Log in as another user and navigate to the previous users profile page | The previous users first name and last name changes can be seen on their profile | As expected | PASS |
| TC032 | [User Story - Manage profile](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87982051&issue=SemMTM%7Cpinterest-clone%7C13) | Other users can see a users profile and their public information | Log in, navigate to another user profile | The user can see the other users profile information | As expected | PASS |
| TC033 |  | 'Created' sections pagination works on page scroll | Log in, upload 20 images, navigate to the profile page and click the "Created" button. Open devtools and check the number of images in the created section, scroll down and more images should be loaded into the DOM | More images are loaded which can be seen in devtools | As expected | PASS |
| TC034 |  | Profile image is displayed in all relevant places after upload | Log in, upload a profile photo, then check the profile page profile photo. Next click on an image you uploaded and make a comment. | Users profile image displayed on profile page, next to users comment and under the users uploaded photo  | As expected | PASS |
| TC035 |  | Can't exceed character limits on edit profile modal inputs | Open the edit profile modal, add 101 characters on first and last name inputs and 601 on about input | User can't type more than the allowed character limit | User can type over character limit | FAIL |
| TC035 #2 |  | Add enforced character limit on HTML form as well as in model | Retry TC035 | Open the edit profile modal, add 101 characters on first and last name inputs and 601 on about input | As expected | PASS |
| TC036 |  | Can't upload a profile image that exceeds the maximum file size | Open edit profile modal, upload a profile photo over 20MB | User gets an error message and file isnt selected | User can upload image greater then max filesize as maxfile size hasnt been set for profile image | FAIL |
| TC036 #2 |  | Add file type and file size validator to Profile model, add client-side validation in JavaScript | Retry TC036 | User gets an error message and file isnt selected | As expected | PASS |
| TC037 |  | Can only upload allowed file types as profile image | Open edit profile modal, try to upload a PDF | User gets an error message and file isnt selected | As expected | PASS |
| TC038 |  | Profile image preview is displayed after image is selected | Open edit profile modal, select a valid image file | Image preview shown after file selected | As expected | PASS |
| TC039 | [User Story - Profile creation](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95979352&issue=SemMTM%7Cpinterest-clone%7C29) | Newly created profiles have a default profile image | Create a new user, navigate to the profile page | Default profile image can be seen on new users profile page | As expected | PASS |
| TC040 |  | Image boards show the number of posts saved to it | Click on a uploaded post, navigate to the users profile page, click on an image board and count the number of images | Image board has the number of pins visisble under it and the number is correct | As expected | PASS |
| TC041 |  | Image boards preview images are shown from images pinned to the board | Log in, upload 3 image, create a board and pin those 3 images. Navigate to the profile page and check the newly created board | The board has the 3 saved images as its thumbnails | As expected | PASS |
| TC042 | [User Story - Manage profile](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87982051&issue=SemMTM%7Cpinterest-clone%7C13) | When edit profile changes are submitted, the profile page is updated dynamically | Open the edit profile modal, make changes to the first and last name then submit | The changes are displayed and the page doesn't refresh | Following error returned: AttributeError: 'CloudinaryResource' object has no attribute 'name' | FAIL |
| TC042 #2 |  | Previously added serverside validation to Cloudinary field caused ValidationError. Removed it and added serverside validation to model:profile profile_image and to ProfileFrom | Retry TC042 | The changes are displayed and the page doesn't refresh | As expected | PASS |
| TC043 | [User Story - Logged in](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95981314&issue=SemMTM%7Cpinterest-clone%7C32) | Profile page button on nav bar only accessible for logged in users | Log in, check the nav bar for the profile page button. Log out, check the nav bar for the profile page button | When logged in, the profile page button is in the nav bar. After logging out, the profile page button is not in the nav bar | As expected | PASS |
| TC044 |  | A non-existant profile cannot be accessed by URL | Navigate to the following url: https://pinterest-clone-sem-29d41bc2ed17.herokuapp.com/profile/1234/ | 404 page displayed | As expected | PASS |
| TC045 |  | 'All Pins' board only accessible by the profile owner | Log out, then navigate to the following url: [User "Sem" All pins board](https://pinterest-clone-sem-29d41bc2ed17.herokuapp.com/profile/board/30/) Next, log in a "Sem" and navigate to the link | 404 page displayed for logged out user, All pins board opened for "Sem" user | As expected | PASS |
| TC045 | [User Story - See all pinned posts](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87986915&issue=SemMTM%7Cpinterest-clone%7C19) | 'All Pins' board shows a list of all posts a user has saved | Create a new user, navigate to the homepage then save 5 images to a new board. Navigate to the profile page and click on the All Pins board | The 5 saved images appear in the all pins board | As expected | PASS |
| TC046 |  | Boards set to private are only visisble by the board owner | Log in as a user "Sem", make a board private then log out. Log in as a new user and navigate to user ["Sem" profile page](https://pinterest-clone-sem-29d41bc2ed17.herokuapp.com/profile/sem/) | The board made private is not visible to the other user but user "Sem" can see it | As expected | PASS |
| TC047 | [User Story Link - Username](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95983218&issue=SemMTM%7Cpinterest-clone%7C31) | You can navigate to a users profile via URL (case-insensetive) | Log out and click the following link to users ["Sem" profile page](https://pinterest-clone-sem-29d41bc2ed17.herokuapp.com/profile/sem/) | Profile page is visible | As expected | PASS |
| **Board Detail Page** |  |  |  |  |  |
| TC048 | [User Story - Another users image boards](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87982835&issue=SemMTM%7Cpinterest-clone%7C15) | Boards can be opened by other users to view pinned posts | Log in as a user and navigate to this [users profile page](https://pinterest-clone-sem-29d41bc2ed17.herokuapp.com/profile/sem/), click and open an image board | The board opens and the pinned images can be seen | As expected | PASS |
| TC049 | [User Story - Open image boards](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87986034&issue=SemMTM%7Cpinterest-clone%7C16) | Masonry grid works as expected on board detail page | Log in as a user and save 10 images to a board, then navigate to the profile page and click on that board | Images in the board are in a masonry grid | As expected | PASS |
| TC050 | [User Story - Manage image boards](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87982570&issue=SemMTM%7Cpinterest-clone%7C14) | Edit board button only appears for board owner | Log out and navigate to the following link ["Sem" profile page "Clothes New" board](https://pinterest-clone-sem-29d41bc2ed17.herokuapp.com/profile/board/27/). Log in as user "Sem" and navigate to "Clothes New" board | Logged out user cannot see "Edit Board" button, user "Sem" can see "Edit Board" button | As expected | PASS |
| TC051 | [User Story - Edit image boards](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95976065&issue=SemMTM%7Cpinterest-clone%7C23) | Board owner can change a boards title |  Log in, create an image board, navigate to the image board, click edit board, change the title | Board title is updated | As expected | PASS |
| TC052 |  | Unpin button only appears for board owner | Log out and navigate to the following link ["Sem" profile page "Clothes New" board](https://pinterest-clone-sem-29d41bc2ed17.herokuapp.com/profile/board/27/). Log in as user "Sem" and navigate to the linked board | Logged out user cannot see unpin buttons, user "Sem" can see unpin buttons | As expected | PASS |
| TC053 | [User Story - Manage image boards](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87982570&issue=SemMTM%7Cpinterest-clone%7C14) | Unpinned image is removed from board | Log in and navigate to a board with images. Unpin an image | Image is removed from the board | As expected | PASS |
| TC054 | [User Story - All pins board](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95979980&issue=SemMTM%7Cpinterest-clone%7C30) | 'All Pins' board cannot be edited by any user | Log in and navigate to the all pins board. Use dev tools to check for edit board modal | Edit board button is hidden and edit board modal is not in the DOM | User can edit all pins board via devtool and modal is in DOM | FAIL |
| TC054 #2 |  | Retry TC054 | Retry TC054 | Edit board button is hidden and edit board modal is not in the DOM | As expected | PASS |
| TC055 | [User Story - All pins board](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95979980&issue=SemMTM%7Cpinterest-clone%7C30) | Edit board button not visisble on 'All Pins' board for any user | Log in and navigate to the all pins board | The edit board button is not visible | As expected | PASS |
| TC056 |  | Deleteing a board removes it from a users profile page | Log in, create a new board, navigate to the newly created board and delete it, navigate back to the profile page | The deleted board is removed from the users profile page | As expected | PASS |
|  | [User Story - Edit image boards](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95976065&issue=SemMTM%7Cpinterest-clone%7C23) | Board owner can change a boards visibility | Log in, navigate to the profile page, click on an image board, open the edit board modal and change the board visisblilty to private. Log out and navigate back to the previous profile page | The board set to private is no longer visisble | As expected | PASS |
| TC057 |  | A deleted board cannot be accessed by URL | Log in, create a board, navigate to the board and copy the link. Delete the board then navigate back to it via the copied link | The link returns a 404 error | As expected | PASS |
| TC058 |  | A private board can only be accessed by the board owner | Log in, create an image board, navigate to it and set its visiblilty to private and refresh the page. Log out and navigate to the users profile page | The logged in user has access to the board, the logged out user cannot see the board on the profile page | As expected | PASS |
| TC059 |  | A user cannot access a private board by URL | Log in, create an image board, navigate to it and set its visiblilty to private, copy the link then log out. After logging out paste the URL into the search bar | The link returns a 404 | As expected | PASS |
| TC060 | [User Story - Edit image boards](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95976065&issue=SemMTM%7Cpinterest-clone%7C23) | Board title changes can be seen by all users | Log in, navigate to a board and change the title. Log out and navigate to that board | The title change can be seen by the logged out user | As expected | PASS |
| TC061 | [User Story - Manage image boards](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87982570&issue=SemMTM%7Cpinterest-clone%7C14) | After a board title is changed, it is updated dynamically | Log in, navigate to an image board and change the title | The board title is changed without page refresh | As expected | PASS |
| TC062 |  | An unpinned image is dyanmically removed from a board | Log in, navigate to an image board with images pinned to it, unpin an image | The image is removed from the board without page refresh | As expected | PASS |
| TC063 | [User Story - Create image boards](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87972960&issue=SemMTM%7Cpinterest-clone%7C10) | A newly saved image is displayed in the correct board | Log in, and open an image from the home page, save that image to a board, navigate to that image board and open it | The saved image is in the correct board | As expected | PASS |
| TC064 | [User Story - All pins board](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95979980&issue=SemMTM%7Cpinterest-clone%7C30) | An image saved to any board is automatically added to the 'All Pins' board | Log in, open a post from the homepage, add the post to an image board, navigate to the profile page and open the "All Pins" board | The image saved to the other board is in the "All Pins" board also | As expected | PASS |
| TC065 | [User Story - Open image boards](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87986034&issue=SemMTM%7Cpinterest-clone%7C16) | The correct posts are displated when clicking into a board | Log in, save 4 posts to a newly created image board, navigate to that image board | The 4 posts can be seen in the image board | As expected | PASS |
| TC0X1 |  | You cannot create a board with the name "All Pins" | Open a post, click save, create a board with the name "All Pins" | Error is thrown and board is not created | Board was created which caused more errors when trying to open profile page as only 1 all pins board should exist | FAIL |
| TC0X1 #2 |  | Add client-side and server-side validation to prevent user from being able to create All Pins board | Retry TC0X1 | Error is thrown and board is not created | As expected | PASS |
| TC0X2 |  | You cannot create a board with an already existing board name | Try and create a board with the same name as one already on your profile page | Error is thrown and board is not created | As expected | PASS |
| TC0X3 |  | You cannot rename a board with an already existing board name | Rename a board with the same name as one already on your profile page | Error is thrown and board is not renamed | Board is renamed | FAIL |
| TC0X3 #2 |  | Add client-side and server-side validation to prevent user from being able rename a board to one that already exists | Retry TC0X3 | Error is thrown and board is not renamed | As expected | Pass |
| TC0X4 |  | You cannot rename a board to All Pins | Rename a board to All Pins | Error is thrown and board is not renamed | Board is renamed | FAIL |
| TC0X4 #2 |  | Add client-side and server-side validation to prevent user from being able rename a board to all pins | Retry TC0X4 | Error is thrown and board is not renamed | As expected | PASS |
| **Post Detail Page** |  |  |  |  |  |
| TC066 | [User Story - Open an image](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87968971&issue=SemMTM%7Cpinterest-clone%7C4) | The correct image is opened on post click | Navigate to the home page and click on a post | The post detail view of the clicked on image is shown | As expected | PASS |
| TC067 | [User Story - Like posts](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95977925&issue=SemMTM%7Cpinterest-clone%7C26) | A logged in user can like a post | Log in, navigate to a post from the home page, click the like button | The user can successfully like the post | As expected | PASS |
| TC068 | [User Story - Like posts](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95977925&issue=SemMTM%7Cpinterest-clone%7C26) | The number of likes a post has can be seen by all users | Log in, like a post, log out, navigate back to the same post | The number of likes can be seen on the post | As expected | PASS |
| TC069 | [User Story - see who uploaded a post](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95978547&issue=SemMTM%7Cpinterest-clone%7C28) | After clicking on a post uploaders profile image, you are taken to their profile page | Navigate to the homepage, click on a post then click on the uploaders username | The user is taken to the uploaders profile page | As expected | PASS |
| TC070 | [User Story - Like posts](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95977925&issue=SemMTM%7Cpinterest-clone%7C26) | A user can remove their like from a post | Log in, navigate to a post, like the post then unlike it | The like was removed from the post | As expected | PASS |
| TC071 | [User Story - Delete a post](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87972680&issue=SemMTM%7Cpinterest-clone%7C9) | A user can delete their own post | Log in, post an image, navigate to the post, copy the url, then delete it the post, paste the URL in the search bar | The user can successfully delete their post and the search returns a 404 | As expected | PASS |
| TC072 | [User Story - Sign In](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95981624&issue=SemMTM%7Cpinterest-clone%7C33) | Any logged in user can comment on a post | Log in, navigate to a post and comment | User can successfully comment | As expected | PASS |
| TC073 | [User Story - Comment on a post](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87969369&issue=SemMTM%7Cpinterest-clone%7C5) | Comments on a post can be seen by all users | Log out and navigate to the post just commented on | You can see the previous users comments | As expected | PASS |
| TC074 | [User Story - Delete other comments](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87986654&issue=SemMTM%7Cpinterest-clone%7C18) | The post owner can delete any comments on their posts | Log in, navigate to a post you own with other users comments, delete a comments from another user | The post owner successfully deletes the users comments | As expected | PASS |
| TC075 | [User Story - Comment date](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95977165&issue=SemMTM%7Cpinterest-clone%7C24) | You can see the amount of time ago a comment was made | Log in, navigate to a users post and comment | Next to the comment the amount of time ago the comment was made can be seen | As expected | PASS |
| TC076 |  | The total number of comments on a post can be seen | Make several comments on a post, count the number of comments on the post | The total number of comments can be seen on the post | As expected | PASS |
| TC077 | [User Story - Delete own comment](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95974819&issue=SemMTM%7Cpinterest-clone%7C21) | A user can delete their own comment | Comment on a post then delete it | The user successfully deletes their comment | As expected | PASS |
| TC078 | [User Story - Edit comment](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87969622&issue=SemMTM%7Cpinterest-clone%7C6) | A user can edit their own comment | Comment on a post then edit the comment | User successfully edits their comment | As expected | PASS |
| TC079 | [User Story - Edit comment](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87969622&issue=SemMTM%7Cpinterest-clone%7C6) | Comment edit can be seen by other users after publishing | Comment on a post, edit the comment, log out and navigate back to the post and find the comment | The comment after the edit can be seen by the logged out user | As expected | PASS |
| TC080 |  | The edit comment button is only displayed for the comment creator | Comment on a post and look for the edit comment button, log out and navigate back to the post | When logged in the user can see the edit button, when logged out the edit button cannot be seen | As expected | PASS |
| TC081 |  | The delete comment button is only displayed for the post owner or the commeter | Comment on a post and look for the delete comment button, log out, navigate back to the post and the comments | Logged in user can see the comment delete button, logged out user cannot see the post delete button | As expected | PASS |
| TC082 |  | The delete post button is only visisble for the post owner | Log in, create a post and navigate to it, log out then navigate back to the post | Logged in user and post owner can see the delete post button, logged out user cannot | As expected | PASS |
| TC083 | [User Story - Pin an image to a board](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87972366&issue=SemMTM%7Cpinterest-clone%7C8) | A user can save a post to a board | Log in, navigate to a post and save it to a board | User can successfully save a post to a board | As expected | PASS |
| TC084 | [User Story - Pin an image to a board](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87972366&issue=SemMTM%7Cpinterest-clone%7C8) | A user can create a new board from the save post modal | Log in, navigate to a post and create a new board from the save post modal. Go to the profile page and locate the newly created board | The user can successfully create a new board and the post is pinned to it | As expected | PASS |
|  | [User Story Link](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95978547&issue=SemMTM%7Cpinterest-clone%7C28) | A user can see who uploaded a post under the image. You can see their profile image and their username | Navigate to a post and open it | User can see uploaders profile name and image | As expected | PASS |
|  | [User Story - profile info on comment](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95977383&issue=SemMTM%7Cpinterest-clone%7C25) | A users comment has their username and profile image next to the comment | Log in, navigate to a post and leave a comment | Users profile image and username can be seen next to their comment | As expected | PASS |
| **Authentication** |  |  |  |  |  |
|  | [User Story - Account registration](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87987195&issue=SemMTM%7Cpinterest-clone%7C20) | A user can sign up with a username and email | Register a new user using a username and email address | A new account is created | As expected | PASS |
| TC085 | [User Story - Logout](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95981777&issue=SemMTM%7Cpinterest-clone%7C34) | Clicking the logout button, logs a user out | Log in, click the log out button | User is logged out | As expected | PASS |
| TC086 | [User Story - Username](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95983218&issue=SemMTM%7Cpinterest-clone%7C31) | When registering, usernames must be unique | Try and create a new user with the username "Sem" | Error message is thrown and account is not created | As expected | PASS |
| TC087 |  | Usernames cannot have URL unsafe characters | Try an create a username with the follwing characters in £$% | Error is thrown and account is not created | As expected | PASS |
| TC088 |  | A user must validate their password correctly to create an account | Create a new account and do not follow password validation rules | Error is thrown and account is not made | As expected | PASS |
| TC089 | [User Story - Sign in](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95981624&issue=SemMTM%7Cpinterest-clone%7C33) | After account creation a user can sign in with their credentials | Create a new account, then sign in with the newly created credentials | User can successfully sign in | As expected | PASS |
| TC090 |  | A user can change their password | Navigate to the profile page, click edit profile, click change password and change the password | user can successfully change their password | As expected | PASS |
| TC091 |  | When creating an account, usernames cannot be blank | Try to create an account with a blank username | As expected | PASS |
| TC092 | [User Story Link - Sign in](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95981624&issue=SemMTM%7Cpinterest-clone%7C33) | A user must be logged in to access the post upload page | Log in then click the new post button in the nav bar. Log out then try to access the create post page. | Logged in user can access the create post page, logged out user is prompted to log in | As expected | PASS |
| TC093 | [User Story - Sign in](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95981624&issue=SemMTM%7Cpinterest-clone%7C33) | A user must be logged in to comment | Login, click on a post from the homepage then leave a comment. Logout and try to comment again. | Logged in user successfully leaves a comment, logged out user is prompted to login | As expected | PASS |
| TC094 | [User Story - Sign in](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95981624&issue=SemMTM%7Cpinterest-clone%7C33) | A user must be logged in to save a post/create a board | Log in, click on a post and save it to an image board. Log out and try to save the post to a board. | Logged in user can save the post, logged out user is prompted to login | As expected | PASS |
| TC095 | [User Story - Login Pop up modal](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=96121167&issue=SemMTM%7Cpinterest-clone%7C39) | The sign-up/log-in page is a pop-up modal | Click the log-in or sign-up button | Log-in modal pops up | As expected | PASS |
| TC096 | [User Story - Logged In](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95981314&issue=SemMTM%7Cpinterest-clone%7C32) | Log in/Sign up buttons hidden for authenticated users in top bar | Log-in with existing credentials | Log-in and sign-up buttons disappear from top bar | As expected | PASS |
| TC097 | [User Story - Logged In](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=95981314&issue=SemMTM%7Cpinterest-clone%7C32) | Sign out button visisble for authenticated users in top bar | Log-in with existing credentials | Log out button now visisble in top bar | As expected | PASS |
| TC098 | [User Story - Account registration](https://github.com/users/SemMTM/projects/2/views/1?pane=issue&itemId=87987195&issue=SemMTM%7Cpinterest-clone%7C20) | Sign up/Log in visisble in top bar for unauthenticated users | Log out of signed in account | Log-in and sign-up buttons are visisble in top bar | As expected | PASS |

## Unit Tests
Extensive unit tests were created for forms and views in each app.

### Post App
- [Views tests](post\test_views.py)
- [Forms tests](post\test_forms.py)

### Profile_page App
- [Views tests](profile_page\test_views.py)

## User Tests

## PageSpeed Insight Testing
PageSpeed Insight testing was performed and found performance to be sub par on a few areas. 
The performance section is expected to be lower due to the large amount of images on the website.

![PageSpeed Tests](<static/readme_images/Screenshot_4.png>)

#### Addressed Issues
The best practices score was lower then expected, the areas targetted for improvment are as follows:

**Issue** 

"Serve static assets with an efficient cache policy"

**Solution**

Add a Long-Term cache policy for Cloudinary image. This was done by adding the following to the end of image src links: 

```|add:'?f_auto,q_auto,cacheControl=public,max-age=31536000'```

**Issue**

"Does not use HTTPS"

**Solution**

Force all Cloudinary images to load as https. This was done by creating a custom template tag that swaps any image url that starts with http to https.

**Issue**

"Properly size images"

**Solution**

Use Cloudinary parameters to integrate dynamic resizing and optimisation of images.

**Issue**

"Document does not have a meta description"

**Solution**

Add meta description to head

**Issue**

If image grid did not resize images fast enough then HTMX trigger "Revealed" would trigger and all pages of images would be loaded then resized.

**Solution**

Load only the first page of images on page load, then the 2nd page after grid resize, then all others on scroll.

## Responsiveness

## Validators
### CSS

### HTML

### Python