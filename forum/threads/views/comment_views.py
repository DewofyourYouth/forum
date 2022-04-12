from urllib.request import Request

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from threads.utils import test_user_permission
from threads.models import *
from threads.serializers import UpdateSerializer
from threads.utils import (
    get_comment,
    get_thread,
    make_unauthorized_response,
    default_invalid_input_response,
    make_not_found_response,
    make_forbidden_response,
)


@authentication_classes([TokenAuthentication])
@api_view(["POST"])
def new(request: Request, thread_id: int) -> Response:
    if not request.user:
        return make_unauthorized_response("no user available")
    thread = get_thread(thread_id)
    if not thread:
        return make_not_found_response(
            f"Couldn't find a thread with the id of {thread_id}"
        )

    serializer = UpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return default_invalid_input_response
    Comment.objects.create(
        title=serializer.data.get("title"),
        content=serializer.data.get("content"),
        user=request.user,
        thread=thread,
    )
    return Response({"message": "comment successfully added."})


@authentication_classes([TokenAuthentication])
@api_view(["DELETE"])
def delete_comment(request: Request, comment_id: int) -> Response:
    comment = get_comment(comment_id)
    if not comment:
        return make_not_found_response(
            f"Couldn't find a comment with the id of {comment_id}"
        )
    if not test_user_permission(request.user, comment.user):
        return make_forbidden_response("Can't delete.")
    title = comment.title
    comment.delete()
    return Response({"message": f"Comment '{title}' was successfully deleted."})


@authentication_classes([TokenAuthentication])
@api_view(["PUT"])
def update_comment(request: Request, comment_id: int) -> Response:
    comment = get_comment(comment_id)
    if not comment:
        return make_not_found_response("Comment not found.")
    if not test_user_permission(request.user, comment.user):
        return make_forbidden_response("You can't update this comment.")
    serializer = UpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return default_invalid_input_response

    if serializer.data.get("title"):
        comment.title = serializer.data["title"]
    if serializer.data.get("content"):
        comment.content = serializer.data["content"]
    comment.save()
    return Response({"message": f"Comment: '{comment.title}' updated successfully."})
