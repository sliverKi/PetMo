from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Bookmark
from posts.serializers import PostListSerializers

class BookmarkSerializers(ModelSerializer):
    print(1)
    post=PostListSerializers(many=True, read_only=True)
    print(2)
    class Meta:
        model=Bookmark
        fields=("post",)