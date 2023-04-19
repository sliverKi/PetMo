from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ParseError
from categories.serializers import BoardSerializers
from pets.serializers import PetsSerializers
from users.serializers import TinyUserSerializers
from .models import Post,Comment

class CommentSerializers(ModelSerializer):
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
        fields=("id","parent_comment", "post", "user", "content","created_at","replies")
    def get_replies(self, obj):
        replies=Comment.objects.filter(parent_comment=obj.id).order_by('created_at')
        serializer=ReplySerializers(replies, many=True)
        return serializer.data
class PostListSerializers(ModelSerializer):#간략한 정보만을 보여줌
    user=TinyUserSerializers()
    pet_category=PetsSerializers(many=True)
    category=BoardSerializers()
    class Meta:
        model=Post
        fields=(
            "pk",
            "category",
            "pet_category",
            "user",
            "created_at", 
            "updated_at",
            "image",
        )

class PostDetailSerializers(ModelSerializer):
    category=BoardSerializers()
    pet_category=PetsSerializers(many=True)
    user=TinyUserSerializers()
    comments=CommentSerializers(many=True)
    
    class Meta:
        model=Post
        fields='__all__'

