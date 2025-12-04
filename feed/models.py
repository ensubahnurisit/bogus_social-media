from django.db import models
import uuid
import os
import random
from django.conf import settings
from shutil import copyfile

# --- Helper function to get random image ---
def random_image_path():
    pictures_dir = os.path.join(settings.BASE_DIR, 'pictures')
    if not os.path.exists(pictures_dir):
        return None
    images = [
        f for f in os.listdir(pictures_dir)
        if os.path.isfile(os.path.join(pictures_dir, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]
    if images:
        chosen_image = random.choice(images)
        media_path = os.path.join(settings.MEDIA_ROOT, 'posts', chosen_image)
        if not os.path.exists(os.path.dirname(media_path)):
            os.makedirs(os.path.dirname(media_path))
        if not os.path.exists(media_path):
            copyfile(os.path.join(pictures_dir, chosen_image), media_path)
        return os.path.join('posts', chosen_image)
    return None

# --- Post Model ---
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_posts')

    def save(self, *args, **kwargs):
        if not self.image:
            image_name = random_image_path()
            if image_name:
                self.image.name = image_name
        super().save(*args, **kwargs)

# --- Comment Model ---
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
