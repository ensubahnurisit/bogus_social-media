from django.shortcuts import render
from .models import Post

def feed_view(request):
    posts = Post.objects.all().order_by('-created_at')  # latest first
    return render(request, "feed/feed.html", {"posts": posts})
