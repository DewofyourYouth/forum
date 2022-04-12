from functools import partial
from rest_framework import status
from rest_framework.response import Response


from threads.models import *


def get_model_by_id(model: models.Model, _id: int) -> models.Model | None:
    try:
        return model.objects.get(id=_id)
    except Exception as e:
        print(e)
        return None


def make_msg_response(
    status: status = status.HTTP_200_OK, msg: str | None = None
) -> Response:
    if not msg:
        return Response(status=status)
    return Response({"message": msg}, status=status)


def test_user_permission(current_user, user_object):
    return user_object == current_user or current_user.is_superuser


get_thread = partial(get_model_by_id, Thread)
get_comment = partial(get_model_by_id, Comment)
make_unauthorized_response = partial(make_msg_response, status.HTTP_401_UNAUTHORIZED)
make_invalid_input_response = partial(make_msg_response, status.HTTP_400_BAD_REQUEST)
make_not_found_response = partial(make_msg_response, status.HTTP_404_NOT_FOUND)
make_forbidden_response = partial(make_msg_response, status.HTTP_403_FORBIDDEN)
default_invalid_input_response = make_invalid_input_response("Invalid input")
