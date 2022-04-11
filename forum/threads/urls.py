from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from threads.views import views
from threads.views import thread_views
from threads.views import comment_views

router = DefaultRouter()
router.register(r"threads", views.ThreadViewSet, "thread")
router.register(r"forum-users", views.ForumUserViewSet, "forum-user")
router.register(r"comments", views.CommentViewSet, "comments")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "delete-thread/<int:thread_id>",
        thread_views.delete_thread,
        name="delete-thread",
    ),
    path(
        "update-thread/<int:thread_id>",
        thread_views.update_thread,
        name="update-thread",
    ),
    path(
        "full-thread/<int:thread_id>",
        thread_views.get_thread_with_comments,
        name="full-thread",
    ),
    path(
        "new-thread",
        thread_views.new,
        name="new-thread",
    ),
    path(
        "delete-comment/<int:comment_id>",
        comment_views.delete_comment,
        name="delete-comment",
    ),
    path(
        "update-comment/<int:comment_id>",
        comment_views.update_comment,
        name="update-comment",
    ),
    path(
        "new-comment/<int:thread_id>",
        comment_views.new,
        name="new-comment",
    ),
]
