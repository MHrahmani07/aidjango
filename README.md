Django Bookstore Project
This is a comprehensive Django web application for a bookstore, featuring CRUD operations for books, user authentication with email verification, favorites, role-based access control, and AI-powered blog post generation using OpenAI.

Table of Contents
Project Description

Features

Project Setup

Prerequisites

Clone the Repository

Create and Activate Virtual Environment

Install Dependencies

Database Setup and Migrations

Create Superuser

Import Sample Book Data

Configure API Keys and Email Settings

Running the Application

Key URLs

Project Structure Overview

Important Notes

Project Description
This Django application serves as a backend and frontend for a bookstore. It allows users to browse a catalog of books, manage their favorite titles, and provides administrative functionalities for managing book data and generating blog content. It demonstrates various Django concepts including Class-Based Views, forms, authentication, and external API integration.

Features
Book Management (CRUD): Create, Read, Update, and Delete book entries.

Book Listing & Details: Display a paginated list of books and detailed views for individual books.

Category Filtering: Filter books by specific categories (e.g., "Persian books", "National computer book").

User Authentication:

User Registration (Sign Up) with email-based OTP (One-Time Password) verification.

User Login (Sign In) with redirection to verification if the account is inactive.

User Logout.

User Profile page displaying basic information and favorited books.

Favorites System: Authenticated users can mark and unmark books as favorites, visible on their profile.

Role-Based Access Control:

Simple Users: Can view books, favorite/unfavorite, and view their profile.

Admin Users (Staff): Can create, edit, and delete books, and generate blog posts.

File Uploads: Admins can upload PDF files and image covers for each book.

AI-Powered Blog Generation:

Admin users can trigger the generation of a new blog post about a random book using the OpenAI API.

Generated blog posts are saved to the database and displayed on a dedicated blog section of the website.

Project Setup
Prerequisites
Python 3.8+

pip (Python package installer)

Clone the Repository
Assuming your project is in a directory named crud_project_root (or similar, where manage.py resides):

# If you were to clone it from a remote repository:
# git clone <repository_url>
# cd <repository_name>

# Assuming you are in the directory containing manage.py already
# (e.g., /home/****/Desktop/project/django/crud/)
# Ensure your directory structure matches:
# .
# ├── crud/                # Django Project (contains settings.py, urls.py)
# ├── book/                # Django App
# ├── blog/                # Django App
# ├── manage.py
# ├── templates/           # Project-level templates
# ├── media/               # Uploaded files will go here
# └── db.sqlite3


Create and Activate Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

python3 -m venv venv
source venv/bin/activate # On Linux/macOS
# venv\Scripts\activate # On Windows


Install Dependencies
Install all necessary Python packages using pip:

pip install Django requests


Database Setup and Migrations
Apply the database migrations to create the necessary tables for your models (Book, BlogPost, VerificationCode, and Django's built-in User/Auth models).

python manage.py makemigrations book
python manage.py makemigrations blog
python manage.py migrate


Create Superuser
Create a superuser account to access the Django administration panel and perform admin-specific actions (like adding/editing books, generating blog posts, and managing users).

python manage.py createsuperuser


Follow the prompts to set a username (e.g., potato), email, and password.

Import Sample Book Data (Optional but Recommended)
To quickly populate your database with test books, use the custom management command. First, ensure you have a books_data.csv file in your project root (next to manage.py).

# books_data.csv (example content, should have 100 entries as discussed)
name,publisher,provider,price,category
The Alchemist,HarperCollins,BookSupply Co.,12.99,other
Python Crash Course,No Starch Press,TechBooks Inc.,35.50,computer
# ... more entries ...


Then, run the command:

python manage.py import_books books_data.csv


Configure API Keys and Email Settings
Open crud/settings.py and modify the following:

SECRET_KEY: Change this to a strong, random string.

EMAIL_HOST_USER: Your Gmail address (or other SMTP user).

EMAIL_HOST_PASSWORD: Your Gmail App Password (or other SMTP password).

DEFAULT_FROM_EMAIL: Your sending email address.

OPENAI_API_KEY: Your actual OpenAI API Key.

# crud/settings.py

# ... (existing settings) ...

SECRET_KEY = 'your-very-secret-and-long-key-here' # CHANGE THIS!

# ... (existing settings) ...

# Email Settings
EMAIL_HOST_USER = 'your_email@gmail.com' # REPLACE
EMAIL_HOST_PASSWORD = 'your_app_password_here' # REPLACE
DEFAULT_FROM_EMAIL = 'your_email@gmail.com' # REPLACE

# OpenAI API Key
OPENAI_API_KEY = 'sk-YOUR_OPENAI_API_KEY_HERE' # REPLACE


Running the Application
Once all setup steps are complete, start the Django development server:

python manage.py runserver


The application will be accessible at http://127.0.0.1:8000/.

Key URLs
Homepage: http://127.0.0.1:8000/

Book List: http://127.0.0.1:8000/book/

Sign Up: http://127.0.0.1:8000/signup/

Log In: http://127.0.0.1:8000/login/

Verify Code: http://127.0.0.1:8000/verify_code/ (You'll be redirected here after signup or if logging in with an inactive account)

User Profile: http://127.0.0.1:8000/profile/

Blog List: http://127.0.0.1:8000/blog/

Django Admin: http://127.0.0.1:8000/admin/

Project Structure Overview
.
├── crud/                      # Django Project Root (formerly bookstore_project)
│   ├── __init__.py
│   ├── settings.py            # Main project settings
│   ├── urls.py                # Main project URL configurations
│   ├── wsgi.py
│   └── asgi.py                # (If present)
├── book/                      # Django App (formerly books)
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── import_books.py # Custom command to import CSV data
│   ├── __init__.py
│   ├── admin.py               # Registers models for Django Admin
│   ├── apps.py
│   ├── models.py              # Book and VerificationCode models
│   ├── forms.py               # BookForm, CodeVerificationForm, CustomUserCreationForm
│   ├── tests.py
│   ├── urls.py                # App-specific URL configurations
│   └── views.py               # All app views (Book CRUD, Auth, Favorites, Code Verification)
├── blog/                      # Django App (for blog posts)
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py               # Registers BlogPost model
│   ├── apps.py
│   ├── models.py              # BlogPost model
│   ├── tests.py
│   ├── urls.py                # App-specific URL configurations
│   └── views.py               # BlogPost list/detail views, OpenAI generation view
├── templates/                 # Project-level templates
│   ├── base.html              # Base HTML template for consistent layout
│   └── registration/          # Templates for authentication (login, signup, verification)
│       └── ...
├── media/                     # Directory for uploaded files (book images, PDFs)
├── manage.py                  # Django's command-line utility
├── books_data.csv             # Sample data for import_books command
├── venv/                      # Python virtual environment
└── db.sqlite3                 # SQLite database file


Important Notes
Security of API Keys/Passwords: For production deployments, never hardcode API keys or sensitive passwords directly in settings.py. Use environment variables or a dedicated secrets management system.

Email Sending: The current setup uses an SMTP server (e.g., Gmail). Ensure your email provider allows "less secure app access" or, preferably, use an "App Password" for security. For robust email in production, consider services like SendGrid, Mailgun, or Amazon SES.

OpenAI Rate Limits: Be mindful of OpenAI's API rate limits. If you trigger the "Generate New Blog Post" button too frequently, you might hit 429 Too Many Requests errors.

Media Files in Production: In a production environment, you would configure a dedicated web server (like Nginx or Apache) or a cloud storage service (like AWS S3 or Google Cloud Storage) to serve media files, rather than relying on Django's development server.

Admin Access: Only users with is_staff=True (like the superuser you create) can access the Django admin panel and perform CRUD operations on books or generate blog posts. Regular users are restricted.
