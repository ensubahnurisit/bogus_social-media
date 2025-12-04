# **📱 Django Social App**

A simple social media web application built with **Django**, featuring:

* User Signup / Login / Logout
* Create Text + Image Posts
* Auto-assign Random Image if No Image is Uploaded
* Inline Like / Unlike System
* Inline Comment System
* Fully Persistent Feed
* PostgreSQL Database
* Django Test Suite Included
* Clean HTML UI with Inline CSS

---

## 🚀 **Features**

### ✔ User Authentication

* Signup
* Login
* Logout
* Duplicate username protection

### ✔ Posts

* Create posts with text
* Upload an image
* If no image is uploaded → random image assigned from `/pictures/` folder
* Posts displayed in a feed ordered by newest first

### ✔ Likes

* Logged-in users can like or unlike any post
* Like count updates instantly
* No refresh of page required to open a separate like page
* Many-to-many relation with users

### ✔ Inline Comments

* Comment box appears directly under each post
* Users can comment without leaving the feed
* All comments are stored with timestamps
* Comment count displayed

### ✔ Fully Styled UI (No frameworks used)

* Modern Facebook-style layout
* Responsive container
* Cards for each post

### ✔ Tests Included

A full Django test suite covering:

* Signup
* Login
* Create post (with and without image)
* Feed ordering
* Commenting
* Likes
* Authentication requirements

---

# 🛠 **Tech Stack**

| Component      | Technology           |
| -------------- | -------------------- |
| Backend        | Django 5             |
| Database       | PostgreSQL           |
| Frontend       | HTML + Inline CSS    |
| Media Handling | Django ImageField    |
| Auth           | Django built-in auth |
| Testing        | Django TestCase      |

---

# 📂 **Project Structure**

```
social_app/
│── feed/
│   ├── templates/feed/
│   │   ├── feed.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── post.html
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── test.py
│── media/
│── pictures/   # used for random auto-images
│── social_app/
│── manage.py
│── README.md
```

---

# ⚙️ **Installation**

## 1️⃣ Clone the Project

```bash
git clone <your-repo-url>
cd social_app
```

---

# 🛢 **PostgreSQL Setup**

Create the database:

```sql
CREATE DATABASE social_app_db;
CREATE USER social_user WITH PASSWORD 'yourpassword';
ALTER USER social_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE social_app_db TO social_user;
```

---

# 📄 **Django Settings**

In `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'social_app_db',
        'USER': 'social_user',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '8888',  # your port
    }
}
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔧 Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# ▶️ Run Server

```bash
python manage.py runserver
```

---

# 🖼 **Random Post Images**

Put any `.jpg / .jpeg / .png` images in:

```
/pictures/
```

When a user posts **without an image**, one of these is randomly assigned.

---

# ❤️ Likes System

In `models.py`:

```python
likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_posts')
```

In `views.py`:

```python
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('feed')
```

---

# 💬 Inline Comments

Each post displays:

* comments list
* comment form directly under the post

`comment_post` view:

```python
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        Comment.objects.create(
            post=post,
            user=request.user,
            content=request.POST.get("content")
        )
    return redirect("feed")
```

---

# 📃 **feed.html (Inline Likes & Comments)**

UI shows:

* Post
* Like/Unlike button
* Comment list
* Comment form inline
* Post image optional

(Full file included in project)

---

# 🧪 Running Tests

```bash
python manage.py test
```

Your test suite includes:

* Authentication tests
* Post creation tests
* Feed ordering
* Image handling
* Inline comment tests
* Like/unlike tests

All tests pass ✔

---

# ✔ TODO / Future Additions

* User profile page
* Notifications
* Direct messaging
* Infinite scrolling feed
* Real-time updates (WebSockets)

---

# 🎉 Final Notes

This project is a **clean, minimal, functional social media platform** built with Django.
It demonstrates:

* Real CRUD functionality
* Auth
* Many-to-many relationships
* File handling
* SQL database integration
* HTML UI
* Automated tests


