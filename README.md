# Pinterest95
Pinterest95 is the first ever version of the now well known social media platform Pinterest. Designed during the days of windows 95, it has a very famililar style and many great features! Pinterest95 is a social media platform that allows users to discover new inspiration for anything and everthing. It is an image sharing platform that allows users to create image/mood boards of posts they like, imteract with images an share posts of their own. 

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

## Agile Planning

## Epics

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