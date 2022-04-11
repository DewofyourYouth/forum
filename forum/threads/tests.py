from django.test import TestCase
from threads.views import *

# Create your tests here.
class TestGetThread(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            "user1", "user1@example.com", "password", is_superuser=True
        )
        user2 = User.objects.create_user(
            "user2", "user2@example.com", "my_safe_password"
        )
        Thread.objects.bulk_create(
            [
                Thread(
                    title="The First Thread",
                    content="Some content.",
                    created_by=User.objects.get(id=1),
                ),
                Thread(
                    title="The Second Thread",
                    content="Some content.",
                    created_by=User.objects.get(id=1),
                ),
                Thread(
                    title="The Third Thread",
                    content="Some content.",
                    created_by=User.objects.get(id=1),
                ),
                Thread(
                    title="The Fourth Thread",
                    content="Some content.",
                    created_by=User.objects.get(id=1),
                ),
                Thread(
                    title="The Fifth Thread",
                    content="Some content.",
                    created_by=User.objects.get(id=1),
                ),
                Thread(
                    title="The Sixth Thread",
                    content="Some content.",
                    created_by=User.objects.get(id=2),
                ),
                Thread(
                    title="The Seventh Thread",
                    content="Some content.",
                    created_by=User.objects.get(id=2),
                ),
                Thread(
                    title="The Eight Thread",
                    content="Some content.",
                    created_by=User.objects.get(id=2),
                ),
                Thread(
                    title="The Ninth Thread",
                    content="Some content.",
                    created_by=User.objects.get(id=2),
                ),
            ]
        )
        thread1 = Thread.objects.get(id=1)
        Comment.objects.bulk_create(
            [
                Comment(
                    user=user1,
                    thread=thread1,
                    title="Comment One",
                    content="this is a comment",
                ),
                Comment(
                    user=user1,
                    thread=thread1,
                    title="Comment Two",
                    content="this is a comment",
                ),
                Comment(
                    user=user1,
                    thread=thread1,
                    title="Comment Three",
                    content="this is a comment",
                ),
            ]
        )

    def test_get_thread(self):
        self.assertEqual("The First Thread", get_thread(1).title)
        self.assertEqual("The Second Thread", get_thread(2).title)

    def test_get_comment(self):
        self.assertEqual("Comment One", get_comment(1).title)
        self.assertEqual("Comment Two", get_comment(2).title)
