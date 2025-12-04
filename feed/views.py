from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Comment

# Home page
def home_view(request):
    return render(request, "feed/home.html")

# Feed page
@login_required(login_url='login')
def feed_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "feed/feed.html", {"posts": posts})

# Signup
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")
        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created! Please login.")
        return redirect("login")
    return render(request, "feed/signup.html")

# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("feed")
        else:
            messages.error(request, "Invalid credentials!")
            return redirect("login")
    return render(request, "feed/login.html")

# Logout
def logout_view(request):
    logout(request)
    return redirect("login")

# Create post
@login_required(login_url='login')
def post_view(request):
    if request.method == "POST":
        content = request.POST.get("content")
        image = request.FILES.get("image")
        if content or image:
            Post.objects.create(user=request.user, content=content, image=image)
        return redirect("feed")
    return render(request, "feed/post.html")

# Like post
@login_required(login_url='login')
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Unlike
    else:
        post.likes.add(request.user)     # Like
    return redirect('feed')

# Comment post
@login_required(login_url='login')
def comment_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        content = request.POST.get("comment")
        if content and content.strip():
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )
        return redirect("feed")

    return redirect("feed")

