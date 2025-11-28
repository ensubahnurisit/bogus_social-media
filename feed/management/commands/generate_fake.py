from django.core.management.base import BaseCommand
from feed.models import User, Post, Comment
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = "Generate fake users, posts, and comments"

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=5, help='Number of users')
        parser.add_argument('--posts', type=int, default=10, help='Number of posts')
        parser.add_argument('--comments', type=int, default=3, help='Number of comments per post')

    def handle(self, *args, **options):
        num_users = options['users']
        num_posts = options['posts']
        num_comments = options['comments']

        self.stdout.write("Generating fake users...")
        users = []
        for _ in range(num_users):
            username = fake.unique.user_name()
            user = User.objects.create(username=username, name=fake.name())
            users.append(user)

        self.stdout.write("Generating fake posts...")
        posts = []
        for _ in range(num_posts):
            author = random.choice(users)
            p = Post.objects.create(
                user=author,
                content=fake.paragraph(nb_sentences=3)
            )
            posts.append(p)

        self.stdout.write("Generating fake comments...")
        for post in posts:
            for _ in range(num_comments):
                commenter = random.choice(users)
                Comment.objects.create(
                    post=post,
                    user=commenter,
                    content=fake.sentence(nb_words=10)
                )

        self.stdout.write(self.style.SUCCESS("Fake data generation complete!"))
