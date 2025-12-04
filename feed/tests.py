
import os
from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from feed.models import Post, Comment

# Temporary media folder for tests
TEST_MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'test_media')

@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class SocialAppFullTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="user1", password="pass1234")
        cls.user2 = User.objects.create_user(username="user2", password="pass5678")

    # -----------------------------
    # AUTH TESTS
    # -----------------------------
    def test_signup_duplicate_username(self):
        response = self.client.post(reverse("signup"), {
            "username": "user1",
            "password": "pass1234"
        })
        self.assertEqual(response.status_code, 302)  # Redirect because username exists

    def test_login_success(self):
        response = self.client.post(reverse("login"), {
            "username": "user1",
            "password": "pass1234"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("feed"))

    def test_logout(self):
        self.client.login(username="user1", password="pass1234")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    # -----------------------------
    # POST CREATION TESTS
    # -----------------------------
    def test_create_post_requires_login(self):
        response = self.client.post(reverse("create_post"), {"content": "Unauthorized"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)

    def test_create_post_without_image(self):
        self.client.login(username="user1", password="pass1234")
        response = self.client.post(reverse("create_post"), {"content": "Hello"})
        self.assertEqual(response.status_code, 302)

        post = Post.objects.first()
        self.assertEqual(post.content, "Hello")
        self.assertIsNotNone(post.image.name)  # Random image automatically assigned

    def test_create_post_with_image(self):
        self.client.login(username="user2", password="pass5678")
        image = SimpleUploadedFile("test.jpg", b"data", content_type="image/jpeg")

        response = self.client.post(reverse("create_post"), {
            "content": "Image Post",
            "image": image
        })
        self.assertEqual(response.status_code, 302)

        post = Post.objects.last()
        self.assertEqual(post.content, "Image Post")
        self.assertTrue(post.image.name.endswith("test.jpg"))

    # -----------------------------
    # FEED TESTS
    # -----------------------------
    def test_feed_loads(self):
        self.client.login(username="user1", password="pass1234")
        response = self.client.get(reverse("feed"))
        self.assertEqual(response.status_code, 200)

    def test_feed_ordering(self):
        self.client.login(username="user1", password="pass1234")

        Post.objects.create(user=self.user1, content="First")
        Post.objects.create(user=self.user2, content="Second")
        Post.objects.create(user=self.user1, content="Third")

        response = self.client.get(reverse("feed"))

        self.assertContains(response, "First")
        self.assertContains(response, "Second")
        self.assertContains(response, "Third")

    # -----------------------------
    # LIKE TESTS
    # -----------------------------
    def test_like_post(self):
        post = Post.objects.create(user=self.user1, content="Like test")

        self.client.login(username="user2", password="pass5678")

        # Like the post
        response = self.client.post(reverse("like_post", args=[post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user2, post.likes.all())

        # Unlike the post
        response = self.client.post(reverse("like_post", args=[post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.user2, post.likes.all())

    def test_like_requires_login(self):
        post = Post.objects.create(user=self.user1, content="Like test")
        response = self.client.post(reverse("like_post", args=[post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(post.likes.count(), 0)

    # -----------------------------
    # COMMENT TESTS
    # -----------------------------
    def test_comment_on_post(self):
        post = Post.objects.create(user=self.user1, content="Comment test")

        self.client.login(username="user2", password="pass5678")
        response = self.client.post(reverse("comment_post", args=[post.id]), {
            "comment": "Nice post!"
        })
        self.assertEqual(response.status_code, 302)

        comment = Comment.objects.last()
        self.assertEqual(comment.content, "Nice post!")
        self.assertEqual(comment.user, self.user2)
        self.assertEqual(comment.post, post)

    def test_comment_requires_login(self):
        post = Post.objects.create(user=self.user1, content="Comment test")
        response = self.client.post(reverse("comment_post", args=[post.id]), {
            "comment": "Unauthorized"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)

    # -----------------------------
    # CLEANUP TESTS
    # -----------------------------
    def tearDown(self):
        for post in Post.objects.all():
            if post.image:
                post.image.delete()
