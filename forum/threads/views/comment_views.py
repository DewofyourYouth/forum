from urllib.request import Request

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from threads.models import *
from threads.serializers import UpdateSerializer
from threads.utils import get_comment, get_thread


@authentication_classes([TokenAuthentication])
@api_view(["POST"])
def new(request: Request, thread_id: int) -> Response:
    if not request.user:
        return Response(
            {"message": "no user available"}, status=status.HTTP_401_UNAUTHORIZED
        )
    thread = get_thread(thread_id)
    if not thread:
        return Response(
            {"message": f"there is no thread with an id of {thread_id}"},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = UpdateSerializer(data=request.data)
    if serializer.is_valid():
        Comment.objects.create(
            title=serializer.data.get("title"),
            content=serializer.data.get("content"),
            user=request.user,
            thread=thread,
        )
        return Response({"message": "comment successfully added."})
    return Response({"message": "invalid input"}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([TokenAuthentication])
@api_view(["DELETE"])
def delete_comment(request: Request, comment_id: int) -> Response:
    comment = get_comment(comment_id)
    if not comment:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if comment.user != request.user and not request.user.is_superuser:
        return Response({"message": "Can't delete"}, status=status.HTTP_403_FORBIDDEN)
    title = comment.title
    comment.delete()
    return Response({"message": f"Comment '{title}' was successfully deleted."})


@authentication_classes([TokenAuthentication])
@api_view(["PUT"])
def update_comment(request: Request, comment_id: int) -> Response:
    comment = get_comment(comment_id)
    if not comment:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if comment.user != request.user and not request.user.is_superuser:
        return Response({"message": "Can't delete"}, status=status.HTTP_403_FORBIDDEN)
    serializer = UpdateSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.data.get("title"):
            comment.title = serializer.data["title"]
        if serializer.data.get("content"):
            comment.content = serializer.data["content"]
        comment.save()
        return Response(
            {"message": f"Comment: '{comment.title}' updated successfully."}
        )
    return Response({"message": "invalid input"}, status=status.HTTP_400_BAD_REQUEST)
