from faker import Faker
from .models import User, Post, Comment
import random

fake = Faker()

def generate_fake_data(user_count=5, post_per_user=3, comment_per_post=2):
    # Create users
    users = []
    for _ in range(user_count):
        username = fake.user_name()
        name = fake.name()
        user = User.objects.create(username=username, name=name)
        users.append(user)

    # Create posts
    posts = []
    for user in users:
        for _ in range(post_per_user):
            post = Post.objects.create(user=user, content=fake.text(max_nb_chars=200))
            posts.append(post)

    # Create comments
    for post in posts:
        for _ in range(comment_per_post):
            commenter = random.choice(users)
            Comment.objects.create(post=post, user=commenter, content=fake.sentence())
