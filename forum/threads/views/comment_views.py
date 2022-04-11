from urllib.request import Request
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from threads.serializers import UpdateSerializer
from threads.models import *
from threads.utils import get_comment


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
    return Response({"message": f"Comment: '{comment.title}' updated successfully."})
