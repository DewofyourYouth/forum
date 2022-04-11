from django.http import HttpResponse
from rest_framework import viewsets
from threads import serializers
from threads.models import *
from threads.serializers import (
    ForumUserSerializer,
    ThreadSerializer,
)


def index(request):
    return HttpResponse("Hello, world. You're at the threads index.")


class ThreadViewSet(viewsets.ModelViewSet):
    serializer_class = ThreadSerializer
    queryset = Thread.objects.all()
    http_method_names = ["get"]


class ForumUserViewSet(viewsets.ModelViewSet):
    serializer_class = ForumUserSerializer
    queryset = User.objects.all()
    http_method_names = [
        "get",
        "post",
    ]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()
    http_method_names = ["get", "post"]
