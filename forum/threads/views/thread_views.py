from urllib.request import Request

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from threads.utils import test_user_permission
from threads.models import *
from threads.serializers import UpdateSerializer
from threads.utils import (
    get_thread,
    make_unauthorized_response,
    default_invalid_input_response,
    make_not_found_response,
    make_forbidden_response,
)


@authentication_classes([TokenAuthentication])
@api_view(["POST"])
def new(request: Request) -> Response:
    if not request.user:
        return make_unauthorized_response("no user available")
    serializer = UpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return default_invalid_input_response

    Thread.objects.create(
        title=serializer.data.get("title"),
        content=serializer.data.get("content"),
        created_by=request.user,
    )
    return Response({"message": "thread successfully added"})


@authentication_classes([TokenAuthentication])
@api_view(["DELETE"])
def delete_thread(request, thread_id: int) -> Response:
    thread = get_thread(thread_id)

    if not thread:
        return make_not_found_response(f"Couldn't find a thread with id {thread_id}")
    if not test_user_permission(request.user, thread.created_by):
        return make_forbidden_response("You can't delete this thread.")

    title = thread.title
    thread.delete()
    return Response({"message": f"Thread: '{title}' was successfully deleted."})


@authentication_classes([TokenAuthentication])
@api_view(["PUT"])
def update_thread(request: Request, thread_id: int) -> Response:
    thread = get_thread(thread_id)
    if not thread:
        return make_not_found_response(f"Couldn't find a thread with id of {thread_id}")
    if not test_user_permission(request.user, thread.created_by):
        return make_forbidden_response(f"Can't delete thread with id {thread_id}")

    serializer = UpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return default_invalid_input_response

    if serializer.data.get("title"):
        thread.title = serializer.data["title"]
    if serializer.data.get("content"):
        thread.content = serializer.data["content"]
    thread.save()
    return Response({"message": f"Thread '{thread.title}' successfully updated."})


@authentication_classes([TokenAuthentication])
@api_view(["GET"])
def get_thread_with_comments(request: Request, thread_id: int) -> Response:
    thread = get_thread(thread_id)
    if not thread:
        return make_not_found_response("Thread not found.")
    comments = thread.comment_set.values(
        "id", "title", "content", "user_id", "user__username", "created_at"
    )
    result = {
        "id": thread_id,
        "title": thread.title,
        "content": thread.content,
        "created_at": thread.created_at,
        "author_id": thread.created_by.id,
        "author": thread.created_by.username,
        "comments": comments,
    }

    return Response(result)
