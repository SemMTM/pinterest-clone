# Pinterest95
The Pinterest95 project is a retro-styled image-sharing and discovery platform inspired by the windows 95 aesthetic, it is a social media platform that allows users to discover new inspiration for anything and everthing. Users can create image/mood boards of posts they like, interact with images, and share posts of their own. 

![Website - Desktop](static/readme_images/Screenshot_11.png)

![Website - Mobile](static/readme_images/Screenshot_12.png)

To use the features of Pinterest95 a user must create and account on log in. Afterwards a user will then be able to:

- Create/Delete posts
- Comment/Like posts
- Create/Edit/Delete image boards
- Save images to image boards

and many other interactive features.

This is a Django-basedd website with all CRUD functionality, agile methodologies were used to plan and implement all features.

The deployed site can be found [HERE](https://pinterest-clone-sem-29d41bc2ed17.herokuapp.com)

# Table of Contents
- [The Strategy Plane](#the-strategy-plane)
    - [Site Goals](#site-goals)
    - [Agile Planning](#agile-planning)
    - [Epics](#epics)
    - [User Stories](#user-stories)
- [The Structure Plane](#the-structure-plane)
    - [Features](#features)
    - [Unimplemented Features](#unimplemented-features)
    - [Future Features](#future-features)
- [The Skeleton Frame](#the-skeleton-plane)
    - [Wireframes](#wireframes)
    - [Database Design](#database-design)
    - [Security](#security)
- [The Surface Plane](#the-surface-plane)
    - [Design](#design)
    - [Colour Scheme](#color-scheme)
    - [Typography](#typography)
- [Technologies](#technologies)
    - [Technology Used](#technology-used)
    - [Python Modules Used](#python-standard-modules)
    - [External Python Modules Used](#external-python-modules)
- [Bugs](#bugs)
    - [Fixed Bugs](#fixed-bugs)
    - [Unfixed Bugs](#unfixed-bugs)
- [Deployment](#deployment)
    - [Version Control](#version-control)
    - [Heroku Deployment](#heroku-deployment)
    - [Run Locally](#run-locally)
    - [Fork Project](#fork-project)
- [Credits](#credits)

# The Strategy Plane

## Site Goals

The primary site goals are to offer users a sharing and disovery experience allowing them to explore content and get visual inspiration seamlessly.

### Functional Goals 

- Image sharing and discovery
    - Users can upload, store, and share images with a community
- User profiles and personalisation
    - Users have their own profile pages which can be customised
- Engagement and interaction
    - Users can interact with other posts, fostering engagement 
- Authentication & account management
    - User can log-in/sign-up
- Search & discoverablilty (not implemented yet)
    - Users can search for posts and explore content based on interest
- Mobile & desktop compatibility
    - The site is designed to be responsive across devices

### User-Centric Goals
- Casual Users
    - Users looking for visual inspiration can browse content effortlessly
    - Intuitive design with aesthetic, nostalgia-driven UI
- Content Creators
    - Provides an easy way to showcase creative work
    - Profile customization and engagement features (likes, comments)
- Community Building
    - Encourages social interaction through likes and comments

### Business & Technmical Goals
- Performance & Scalability
    - Use cloud-based image hosting for faster image serving
    - Database optimisation such as UUIDs for posts (better indexing and scalability)
- Security & Privacy
    - CSRF protection and authentication handled by Django Allauth.
- Potential Monetisation and Growth
    - Possible future ad-based revenue model
    - Could expand with premium profiles or exclusive content features

# The Scope Plane
## Agile Planning

This project was developed using agile methodologies by delivering small features in incremental sprints. As this was my first full-stack project I did not know how long each feature would take to implement due to lack of experience, as a result the sprints were not given a time frame individually. The total time for all features to be impementated was 2 months. The long time frame was to allow for a lack of efficiency while I gained more experince with Django and the whole process of developing a full-stack application.

All user stories were assigned to epics, prioritised under the labels, Must have, Should have and Could have. "Must have" stories were the most important fetures and were subsequently implemented first, then the "Should haves" were implemented and finally the "Could haves". Some "Could haves" were not implemented due to time constraints. Feature implementation was done this way to ensure all core requirments were implemented first, with nice to have features being added with available capacity.

The Product Backlog was created using Github projects and can be located [HERE](https://github.com/users/SemMTM/projects/2/views/1). All user stories have acceptance criteria in order to define the functionality that marks that story as complete.

![Product Backlog](static/readme_images/Screenshot_13.png)

## Epics

This project had 7 main epics that user stories were catagorised into:

#### Authentication
The Authentication epic is for all user stories pertaining to user authentication and registration. This epic provides crutial functionaliy and security to the app and users. Without user authentication almost of all the features Pinterest95 currently has would not be do-able.

#### Backend
The Backend epic is for all stories related to the set up of the project and database. Another critical epic as without the server-side set up or database the app would not function.

#### Comments
The Comments epic is for all user stories related to the comment functionailty. This includes, creating, editing, deleteing comments and other minor comment related features.

#### Home Page
The Home Page epic is for all user stories related to the home page. This is particularly important as this is the area where users will discover new content and spend most of their time. This epic includes all user stories related to the masonry grid layout and implementation as well as the nav bar.

#### Image Boards
The Image Boards epic is for all user stories relating to the mood boards of images that users can create. A big part of the goals of the app is to help users get visual inspiration, allowing users to save and collect images into one area that they can specify and customise is cruital to the user experience.

#### Posts
The Post epic is for user stories related to post creation, deletion, like, image tags etc.

#### Profile
The Profile epic is for all user stories related to the users own profile page. The profile page is where users can customise their experince and is the area that other users can also see. This page shows the users public image boards, all posts they have created, their public profile info and more.

## User Stories

#### Authentication
- As a user I can Sign in/Log in via a pop up modal so that I don't need to go to a new page to sign in
- As a user I can log out
- As a user I can sign in to the app so that I can use all of its features
- As a user I can tell if I am logged in so that I can log in if needed
- As a user I can create an account so that I can use all of the sites features

#### Backend
- As a developer I need to create my database models so that I can store and access information for the app to function
- As a developer I need to set up all auth so that my app can have user authentication
- As a developer I need to connect my app to my SQL database so that I can store information to create the app
- As a developer I need to set up cloudinary so that users can upload images

#### Comments
- As a user I can see how long ago a comment was made so that I know how old a comment is
- As a user I can see left a specific comment on an image so that I know who left the comment
- As a user I can delete one of my comments from a post
- As a user I can edit or delete comments I have made so that I can interact with other users
- As a user I can delete comments on my post so that I can manage my content better
- As a user I can comment on a post so that I can interact with other users

#### Home Page
- As a user I can search for image themes so that I can find related images (not implemented)
- As a user I can find images by clicking tags so that I can find content related to the tag (not implemented)
- As a User I can access a nav bar so that I can go to different pages on the website
- As a user I can see posts in a masonry grid so that my user experience is better
- As a user I can see a list of images so that select which image I would like to open

#### Image Boards
- As a developer I can create a blank "All Pins" board for every user so that they can see all their pinned images
- As a user I can edit an image boards visibility and title so that I have more control over my experience
- As a user I can see an image board with all of my pinned images so that I can go through my pins quickly
- As a user I can open image boards so that I can see a list of the images saved to it
- As a user I can edit my image boards so that I can customise them to my preferences
- As a user I can create image boards so that I can save images to it and view them later

#### Posts
- As a developer I can convert image to JPEG and compress them before upload so that image load much faster for users
- As a user I can tag an image with image tags so that other users can see what the post is about
- As a user I can like an image so that I can interact with posts I enjoy
- As a user I can see who uploaded a post so that I can go to their profile and see more about the user
- As a user I can delete my posts so that I can remove posts I don't want to be uploaded anymore
- As a user I can pin images to one of my image boards so that I can see all images in one place
- As a user I can create a post so that I can share content
- As a User I can Open a post so that view it in greater detail

#### Profile
- As a user I can have a unique username so that users can find my profile
- As a developer I can create a blank user profile with a default image when a user is created
- As a User I can edit my profile information so that I can manage my profile
- As a user I can see image boards other users have created so that I can look through their saved images
- As a user I can view my created posts so that I can manage them
- As a user I can view a users profile so that I can interact with other users
- As a user I can see a list of my and other users created image boards on the profile so that I can view image collections

[Back to Table of Contents](#table-of-contents)

# The Structure Plane

## Features

### Feature 1
#### Description
#### Implementation
#### User Stories Completed

## Unimplemented Features

## Future Features

[Back to Table of Contents](#table-of-contents)

# The Skeleton Plane

## Wireframes

## Database Design

## Security

[Back to Table of Contents](#table-of-contents)

# The Surface Plane

## Design

## Color Scheme

## Typography

[Back to Table of Contents](#table-of-contents)

# Technologies

## Technology Used
This project utilizes a combination of **programming languages, frameworks, and development tools** to ensure **scalability, performance, and maintainability**.

| **Technology** | **Use Case in Project** |
|--------------|------------------------|
| **Python** | Used as the primary programming language for the backend, handling logic, database interactions, and API endpoints. |
| **Django** | Backend web framework responsible for handling user authentication, database management, and API routing. |
| **PostgresSQL** | The relational database management system (RDBMS) used to store user data, posts, comments, and other project-related content. |
| **HTMX** | Enables dynamic content loading and AJAX-like interactions without writing JavaScript. Used for infinite scrolling, modals, and partial page updates. |
| **JavaScript** | Used for handling real-time UI updates, form validation, grid resizing, and client-side interactions. |
| **HTML** | Defines the structure of the web pages and is dynamically rendered using Django templates. |
| **CSS** | Handles styling, layout, and responsiveness across all devices. |
| **Visual Studio Code** | The main code editor used for development, debugging, and testing. |
| **GitHub** | Used for version control, collaboration, and storing project code in a remote repository. |
| **Git** | Used for local version control, allowing developers to commit, branch, and push changes efficiently. |
| **Heroku** | Cloud platform used for deploying and hosting the live application. Ensures high availability and scalability. |

### HTML
HTML provides the structure for web pages and is dynamically rendered through Django templates.

- Uses **template inheritance** for consistency across pages.
- Includes **HTMX attributes** for partial updates and interactions.

### HTMX
HTMX is used to enhance user interactions by enabling AJAX-like functionality without writing JavaScript. It allows the server to return only the necessary HTML fragments, which are then dynamically updated on the page.

| Features | HTMX Useage |
|----|----|
| **Infinite Scrolling for Posts** | HTMX loads new images dynamically when the user scrolls to the bottom of the page `hx-trigger="revealed"` |
| **Masonry Grid Resizing** | HTMX swaps in image content and then resizes the grid dynamically after images load |
| **Profile Editing Modal** | Updates the profile without a full page reload (`hx-get` to load the form, `hx-post` to submit changes) |
| **Like Button Updates** | HTMX sends AJAX-like requests to like/unlike a post without reloading the page |
| **Dynamic Board Content** | HTMX fetches and updates board-related images and details when interacting with UI elements |

### CSS
CSS is responsible for styling and layout consistency.

- Implements **responsive design** to ensure usability across all devices.
- Used to style the entire website via an external file.

### JavaScript
JavaScript is used in this project to handle client-side interactions, dynamic UI updates, and performance optimizations.

| **Feature**                     | **Description** |
|---------------------------------|---------------|
| **Masonry Grid Resizing & Optimization** | Ensures images load properly before resizing the grid, preventing layout shifts and improving performance. Dynamically resizes grid items based on image dimensions to maintain a consistent layout. |
| **Lazy Loading & Infinite Scroll** | Dynamically loads content only when needed to improve performance. The first page of images loads on page load, and subsequent pages are loaded as the user scrolls. |
| **Like Button Handling**        | Updates likes instantly without requiring a full page reload. |
| **Comment System**              | Allows users to add, edit, and delete comments with real-time UI updates. |
| **Profile Image Upload Validation** | Prevents uploading unsupported file types and large images before submission. |
| **Post Creation Form Validation** | Enforces character limits and prevents users from exceeding them while typing. |
| **Board Creation & Renaming Validation** | Prevents users from creating or renaming boards to restricted names like "All Pins" and checks for duplicate board names (case insensitive). |
| **Form Submission Prevention on Empty Fields** | Ensures required fields are filled before form submission to improve user experience. |
| **Modal Management**            | Handles opening and closing of modals for editing profiles, boards, and viewing comments dynamically. |
| **Board Management**            | Prevents duplicate board names and restricted names like "All Pins." |

### Python
Python is the core programming language used in this project. It provides **fast development, readable syntax, and extensive library support** for web applications.

- Used in **Django** for backend logic, database queries, and API development.
- Handles **user authentication, data processing, and server-side validation**.
- Integrates with **HTMX and JavaScript** to deliver dynamic user experiences.

### Visual Studio Code
VS Code is the **primary development environment** for writing, debugging, and testing the project.

- Used with **ESLint, Prettier, and Python extensions** for improved code quality.
- Integrated with **Git and GitHub** for version control.
- Supports **virtual environments and Django development tools**.

### GitHub
GitHub is used for **version control, collaboration, and deployment integration**.

- Stores the **entire project codebase** in a remote repository.
- Tracks **issues, pull requests, and project progress**.
- Automates deployments using **GitHub Actions**.

### Git
Git is used for **local version control**, allowing developers to track changes and collaborate effectively.

- Used to **commit, branch, merge, and push code to GitHub**.
- Ensures that **new features and fixes are properly integrated** before deployment.
- Prevents accidental data loss through **history tracking**.

### Heroku
Heroku is the **cloud platform used for deployment**.

- Hosts the **Django application and serves the frontend**.
- Manages **automatic scaling, database integration, and environment configurations**.
- Secures traffic with **SSL/HTTPS encryption**.

### Django
Django is the **backend framework** used to **handle authentication, database operations, and API routing**.

- Implements **user authentication, post creation, and comments**.
- Manages **database queries efficiently using the Django ORM**.
- Handles **server-side validation and security best practices**.

### PostgresSQL
MySQL is the **relational database** used to **store structured data**.

- Stores **user data, posts, comments, likes, and boards**.
- Optimized for **fast queries and relational integrity**.
- Integrated with Django using **MySQLClient and Django ORM**.


## Python Standard Modules
- `datetime`
- `os`
- `sys`
- `json`
- `uuid`
- `collections`
- `math`
- `pathlib`
- `threading`
- `sqlite3`
- `subprocess`

## External Python Modules
| Package | Version | Description |
|----------|----------|------------|
| `asgiref` | 3.8.1 | ASGI support for Django |
| `certifi` | 2024.12.14 | SSL Certificates for Requests |
| `charset-normalizer` | 3.4.1 | Encoding detection |
| `cloudinary` | 1.41.0 | Cloud Storage for Images |
| `dj-database-url` | 2.3.0 | Database URL Parser for Django |
| `dj3-cloudinary-storage` | 0.0.6 | Cloudinary storage for Django |
| `Django` | 5.1.3 | Web Framework |
| `django-allauth` | 65.3.0 | User Authentication and Social Login |
| `django-crispy-forms` | 2.3 | Django Forms Styling |
| `django-extensions` | 3.2.3 | Extra Django Utilities |
| `django-htmx` | 1.21.0 | HTMX Support for Django |
| `gunicorn` | 23.0.0 | WSGI Server for Deployment |
| `idna` | 3.10 | Internationalized Domain Names Support |
| `mysqlclient` | 2.2.6 | MySQL Database Adapter for Django |
| `packaging` | 24.2 | Package Metadata Handling |
| `Pillow` | 11.1.0 | Image Processing |
| `pip` | 25.0.1 | Python Package Manager |
| `psycopg2` | 2.9.10 | PostgreSQL Database Adapter for Django |
| `requests` | 2.32.3 | HTTP Requests Library |
| `six` | 1.17.0 | Python 2 and 3 Compatibility |
| `sqlparse` | 0.5.2 | SQL Parser for Django |
| `tornado` | 6.4.2 | Scalable Web Server |
| `typing_extensions` | 4.12.2 | Backports for Type Hints |
| `tzdata` | 2025.1 | Timezone Data |
| `urllib3` | 2.3.0 | HTTP Client for Requests |
| `whitenoise` | 6.8.2 | Static File Serving |

[Back to Table of Contents](#table-of-contents)

# Bugs

## Fixed Bugs

## Unfixed Bugs

[Back to Table of Contents](#table-of-contents)

# Deployment

## Version Control

## Heroku Deployment

## Run Locally

## Fork Project

[Back to Table of Contents](#table-of-contents)

# Credits


### Credits:
- How to pin navbar to the bottom of the screen: https://forum.builder.io/t/how-do-you-pin-a-nav-bar-to-the-bottom-of-the-screen/32
- CSS Masonry layout: https://kulor.medium.com/pinterest-style-masonry-layout-using-pure-css-493c1206d01d
- CSS image overlay: https://www.w3schools.com/howto/howto_css_image_overlay_title.asp
- Infinite scroll in Django using HTMX: https://www.fmacedo.com/posts/1-django-htmx-infinite-scroll
- Horizontal masonry using JavaScript: https://medium.com/@andybarefoot/a-masonry-style-layout-using-css-grid-8c663d355ebb
- How to call a function inside a template: https://stackoverflow.com/questions/57832308/how-do-you-call-a-javascript-function-inside-a-django-template
- show image in admin - https://dev.to/vijaysoni007/how-to-show-images-of-the-model-in-django-admin-5hk4
- How to get user id - https://stackoverflow.com/questions/6898260/django-user-id-fields
- Coding help through the entire project - ChatGPT