from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from threads.models import Thread, Comment
from threads.views import *
from threads.utils import get_thread, get_comment
from threads.views.thread_views import delete_thread, test_user_permission

# Create your tests here.
class TestGetThread(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            "user1", "user1@example.com", "password", is_superuser=True
        )
        self.user1.is_superuser = True
        self.user1.save()
        self.user2 = User.objects.create_user(
            "user2", "user2@example.com", "my_safe_password"
        )
        Thread.objects.bulk_create(
            [
                Thread(
                    title="The First Thread",
                    content="Some content.",
                    created_by=self.user1,
                ),
                Thread(
                    title="The Second Thread",
                    content="Some content.",
                    created_by=self.user1,
                ),
                Thread(
                    title="The Third Thread",
                    content="Some content.",
                    created_by=self.user1,
                ),
                Thread(
                    title="The Fourth Thread",
                    content="Some content.",
                    created_by=self.user1,
                ),
                Thread(
                    title="The Fifth Thread",
                    content="Some content.",
                    created_by=self.user1,
                ),
                Thread(
                    title="The Sixth Thread",
                    content="Some content.",
                    created_by=self.user2,
                ),
                Thread(
                    title="The Seventh Thread",
                    content="Some content.",
                    created_by=self.user2,
                ),
                Thread(
                    title="The Eighth Thread",
                    content="Some content.",
                    created_by=self.user2,
                ),
                Thread(
                    title="The Ninth Thread",
                    content="Some content.",
                    created_by=self.user2,
                ),
            ]
        )
        thread1 = Thread.objects.get(id=1)
        Comment.objects.bulk_create(
            [
                Comment(
                    user=self.user1,
                    thread=thread1,
                    title="Comment One",
                    content="this is a comment",
                ),
                Comment(
                    user=self.user1,
                    thread=thread1,
                    title="Comment Two",
                    content="this is a comment",
                ),
                Comment(
                    user=self.user1,
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

    def test_get_thread_with_comments(self):
        c = Client()
        response = c.get("/threads/full-thread/1")
        self.assertEqual("user1", response.data["author"])
        self.assertEqual(3, response.data["comments"].count())
        response = c.get("/threads/full-thread/6")

    def test_test_user_permission(self):
        thread1 = Thread.objects.get(id=1)
        thread6 = Thread.objects.get(id=6)
        self.assertTrue(test_user_permission(self.user2, thread6.created_by))
        self.assertTrue(test_user_permission(self.user1, thread6.created_by))
        self.assertFalse(test_user_permission(self.user2, thread1.created_by))
        self.assertTrue(test_user_permission(self.user1, thread1.created_by))

    def test_delete_thread_allowed_by_owner(self):
        self.client.login(username="user2", password="my_safe_password")
        response = self.client.delete("/threads/delete-thread/6")
        self.assertEqual(200, response.status_code)

    def test_delete_thread_allowed_by_superuser(self):
        self.client.login(username="user1", password="password")
        response = self.client.delete("/threads/delete-thread/6")
        self.assertEqual(200, response.status_code)

    def test_delete_thread_not_allowed(self):
        self.client.login(username="user2", password="my_safe_password")
        response = self.client.delete("/threads/delete-thread/1")
        self.assertEqual(403, response.status_code)
