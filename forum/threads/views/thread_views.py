import json
from pprint import pprint
from django.core.serializers.json import DjangoJSONEncoder
from urllib.request import Request
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from threads.serializers import ThreadSerializer
from threads.serializers import UpdateSerializer
from threads.models import *
from threads.utils import get_thread


@authentication_classes([TokenAuthentication])
@api_view(["POST"])
def new(request: Request):
    if not request.user:
        return Response(
            {"message": "no user available"}, status=status.HTTP_401_UNAUTHORIZED
        )
    serializer = UpdateSerializer(data=request.data)
    if serializer.is_valid():
        pprint(serializer.data)
        Thread.objects.create(
            title=serializer.data.get("title"),
            content=serializer.data.get("content"),
            created_by=request.user,
        )
        return Response({"message": "thread successfully added"})
    return Response({"message": "invalid input"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_thread(request, thread_id: int) -> Response:
    thread = get_thread(thread_id)
    if not thread:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if thread.created_by != request.user and not request.user.is_superuser:
        return Response({"message": "Can't delete"}, status=status.HTTP_403_FORBIDDEN)

    title = thread.title
    thread.delete()
    return Response({"message": f"Thread: '{title}' was successfully deleted."})


@api_view(["PUT"])
def update_thread(request: Request, thread_id: int) -> Response:
    thread = get_thread(thread_id)
    if not thread:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if thread.created_by != request.user and not request.user.is_superuser:
        return Response({"message": "Can't delete"}, status=status.HTTP_403_FORBIDDEN)

    serializer = UpdateSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.data.get("title"):
            thread.title = serializer.data["title"]
        if serializer.data.get("content"):
            thread.content = serializer.data["content"]
        thread.save()
    return Response({"message": f"Thread '{thread.title}' successfully updated."})


@api_view(["GET"])
def get_thread_with_comments(request: Request, thread_id: int) -> Response:
    thread = get_thread(thread_id)
    comments = thread.comment_set.values(
        "id", "title", "content", "user_id", "user__username"
    )
    result = {
        "id": thread_id,
        "title": thread.title,
        "content": thread.content,
        "author_id": thread.created_by.id,
        "author": thread.created_by.username,
        "comments": comments,
    }

    return Response(result)
