from django.shortcuts import render, redirect
from .models import Post

# Home page
def home_view(request):
    return render(request, "feed/home.html")

# Feed page
def feed_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "feed/feed.html", {"posts": posts})

# Login page
def login_view(request):
    if request.method == "POST":
        return redirect("feed")
    return render(request, "feed/login.html")

# Signup page
def signup_view(request):
    if request.method == "POST":
        return redirect("feed")
    return render(request, "feed/signup.html")

# Post creation page
def post_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        Post.objects.create(user=request.user, content=content, image=image)
        return redirect('feed')
    return render(request, 'feed/post.html')

# Likes/comments placeholders
def like_post(request, post_id):
    return redirect('feed')

def comment_post(request, post_id):
    return redirect('feed')
