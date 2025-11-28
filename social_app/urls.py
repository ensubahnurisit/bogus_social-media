from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from feed.views import (
    home_view, feed_view, post_view,
    login_view, signup_view, like_post, comment_post
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),          # Home page
    path('feed/', feed_view, name='feed'),     # Feed page
    path('login/', login_view, name='login'),  # Login page
    path('signup/', signup_view, name='signup'), # Signup page
    path('post/', post_view, name='create_post'), # Create post page
    path('post/<uuid:post_id>/like/', like_post, name='like_post'),
    path('post/<uuid:post_id>/comment/', comment_post, name='comment_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
