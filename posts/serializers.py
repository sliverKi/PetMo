from rest_framework import status
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from categories.serializers import BoardSerializers
from pets.serializers import PetsSerializers
from users.serializers import TinyUserSerializers
from .models import Post,Comment
import sys
sys.setrecursionlimit(100000)
class CommentSerializers(ModelSerializer):
    # replies=serializers.SerializerMethodField()
    class Meta:
        model=Comment
        fields="__all__"     

class CommentDetailSerializers(ModelSerializer):
    class Meta:
        model=Comment
        fields='__all__'


class ReplySerializers(ModelSerializer):
    replies=serializers.SerializerMethodField()
    class Meta:
        model=Comment
        fields=(
            "id",
            "parent_comment",
            "post",  
            "user",
            "content",
            "created_at",
            "replies",
        )
    
    def get_replies(self, obj):
        replies=Comment.objects.filter(parent_comment=obj.id).order_by('created_at')
        if not replies.exists():
            return None
        serializer=ReplySerializers(replies, many=True,)
        return serializer.data
class PostSerializers(ModelSerializer):
    user=TinyUserSerializers(read_only=True)
    class Meta:
        model=Post
        fields=(
            "pk",
            "user",
            "content",
            "image",
            "category",
            "pet_category",
        )
    def validate(self, data):
        content = data.get('content', None)
        image = data.get('image', None)

        if content is None and image is None:
            raise ParseError({"error": "내용을 입력해주세요."})
        return data
class PostListSerializers(ModelSerializer):#간략한 정보만을 보여줌
    user=TinyUserSerializers(read_only=True)
    pet_category=PetsSerializers(many=True)
    category=BoardSerializers()
    class Meta:
        model=Post
        fields=(
            "pk",
            "category",
            "pet_category",
            "user",
            "content",
            "created_at", 
            "updated_at",
            "image",
        )

class PostDetailSerializers(ModelSerializer):
    category=BoardSerializers()
    pet_category=PetsSerializers(many=True)
    user=TinyUserSerializers()
    comments=ReplySerializers(many=True)
    
    class Meta:
        model=Post
        fields=(
            "id",
            "category",
            "pet_category",
            "user", 
            "content",
            "comments",
            "created_at",
            "updated_at",
            "content",
            "image",
        )

