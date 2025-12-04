# Mini Social App

A simple social media web application built with Django that allows users to sign up, log in, create posts with optional images, view a feed, and see comments.  

---

## Features Implemented

### User Authentication
- Signup with username and password.
- Login/logout functionality.
- Passwords are securely stored using Django’s authentication system.
- Messages for successful login/signup or errors.

### Posts
- Users can create posts with text content and optional images.
- Automatically assigns a random image if no image is uploaded.
- Posts are displayed in reverse chronological order on the feed.
- Only posts from valid users are displayed.

### Comments & Likes (Placeholders)
- Comment and like functionality added as placeholders for future implementation.

### Database
- Models:
  - `User` – Stores username and name.
  - `Post` – Stores post content, image, user, timestamp.
  - `Comment` – Stores comment content, related post, user, timestamp.
- Handled foreign key constraints and orphaned data during migrations.

### Frontend
- Simple, responsive design using inline CSS.
- Login and signup forms with centered placeholders.
- Feed displays posts with rounded cards, shadows, and optional images.
- Navigation links for Home, Feed, Post, Login, Signup.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository_url>
cd social_app
python manange.py runserver
in another terminal open - python genrate_fake.py to create a fake FEED .
