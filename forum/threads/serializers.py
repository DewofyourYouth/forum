from rest_framework import serializers
from threads.models import *


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ["id", "title", "content", "created_at"]


class ForumUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class UpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    content = serializers.CharField(required=False)
