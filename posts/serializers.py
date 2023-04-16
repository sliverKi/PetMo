
from rest_framework.serializers import ModelSerializer
from categories.serializers import BoardSerializers
from pets.serializers import PetsSerializers
from users.serializers import TinyUserSerializers
from .models import Post,Comment

class CommentSerializers(ModelSerializer):
    class Meta:
        model=Comment
        fields="__all__" 

class PostListSerializers(ModelSerializer):#간략한 정보만을 보여줌
    user=TinyUserSerializers()
    pet_category=PetsSerializers(many=True)
    category=BoardSerializers()
    class Meta:
        model=Post
        fields=(
            "pk",
            "user",
            "pet_category",
            "category",
            "created_at", 
            "updated_at",
            "image",
        )

class PostDetailSerializers(ModelSerializer):
    user=TinyUserSerializers()
    pet_category=PetsSerializers(many=True)
    category=BoardSerializers()
    comments=CommentSerializers(many=True)
    
    class Meta:
        model=Post
        fields='__all__'

