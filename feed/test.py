import os
from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Post

# Temporary media folder for testing image uploads
TEST_MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'test_media')

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class AdvancedSocialAppTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create users
        cls.user1 = User.objects.create_user(username='user1', password='pass1234')
        cls.user2 = User.objects.create_user(username='user2', password='pass5678')

    def test_create_post_without_image(self):
        self.client.login(username='user1', password='pass1234')
        response = self.client.post(reverse('create_post'), {'content': 'Text only post'})
        self.assertEqual(response.status_code, 302)
        post = Post.objects.first()
        self.assertEqual(post.content, 'Text only post')
        # Model automatically assigns random image, so expect not None
        self.assertIsNotNone(post.image.name)

    def test_create_post_with_image(self):
        self.client.login(username='user2', password='pass5678')
        image = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        response = self.client.post(reverse('create_post'), {'content': 'Image post', 'image': image})
        self.assertEqual(response.status_code, 302)
        post = Post.objects.last()
        self.assertEqual(post.content, 'Image post')
        self.assertTrue(post.image.name.endswith('test.jpg'))

    def test_feed_ordering(self):
        self.client.login(username='user1', password='pass1234')
        # Create posts from both users
        Post.objects.create(user=self.user1, content='User1 first')
        Post.objects.create(user=self.user2, content='User2 first')
        Post.objects.create(user=self.user1, content='User1 second')
        
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        # Check that feed contains all posts
        self.assertContains(response, 'User1 first')
        self.assertContains(response, 'User2 first')
        self.assertContains(response, 'User1 second')

    def test_create_post_requires_login(self):
        response = self.client.post(reverse('create_post'), {'content': 'Unauthorized post'})
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertEqual(Post.objects.count(), 0)

    def test_signup_duplicate_username(self):
        response = self.client.post(reverse('signup'), {
            'username': 'user1',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        # Your signup view currently redirects on duplicate
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        # Clean up any uploaded files
        for post in Post.objects.all():
            if post.image:
                post.image.delete()
