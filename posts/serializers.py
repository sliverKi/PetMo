from rest_framework import status
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from categories.serializers import BoardSerializers
from pets.serializers import PetsSerializers
from users.serializers import TinyUserSerializers
from .models import Post,Comment, Image
from categories.models import Category
from pets.models import Pet
import sys
sys.setrecursionlimit(100000)
class ImageSerializers(ModelSerializer):
    class Meta:
        model=Image
        fields=(
            "id",
            "image",
        )


class CommentSerializers(ModelSerializer):
    class Meta:
        model=Comment
        fields=( 
            "id",
            "parent_comment",
            "post",  
            "user",
            "content",
            "created_at",
            "updated_at",
        ) 


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
            "updated_at",
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
    image=ImageSerializers(many=True)
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
    image=ImageSerializers(many=True)#첫번째 이미지만 보여줌 

    class Meta:
        model=Post
        fields=(
            "pk",
            "category",
            "pet_category",
            "user",
            "content",
            "image",
            "created_at", 
            "updated_at",
        )
    def validate_image(self, data):
        print(1)
        image= data.get('image', None)
        if len(image)>2:
            return image[0]

class PostDetailSerializers(ModelSerializer):#image 나열
    user=TinyUserSerializers()
    pet_category=PetsSerializers(many=True)
    category=BoardSerializers()
    image=ImageSerializers(many=True)
    
    class Meta:
        model=Post
        fields=(
            "id",
            "category",
            "pet_category",
            "user", 
            "content",
            "image",
            "created_at",
            "updated_at",    
        )


    #{ update()-put()
    #"content": "test",
    #"category": {"type": "Free"},
    #"pet_category": [{"species": "cat"}, {"species":"dog"}, {"species":"fish"}]
    #}
    # image : 다중 이미지 만들기. 
    def update(self, instance, validated_data):
        
        instance.pet_category.clear()
        pet_category_data = validated_data.pop("pet_category", None)
        image_data = validated_data.pop("image", None)
        category_data = validated_data.pop("category", None)
        # print("q: ", category_data)
        if category_data is not None:
            category_instance = Category.objects.filter(type=category_data.get("type")).first()
            # print("a: ", category_instance)
            if category_instance is None:
                raise serializers.ValidationError({"category": "Invalid category"})
            instance.category = category_instance

        # Update the remaining fields
        instance = super().update(instance, validated_data)

        # Update the many-to-many fields
        if pet_category_data is not None:
            for pet_category in pet_category_data:
                species = pet_category.get("species")
                if species:
                    pet_category, _ = Pet.objects.get_or_create(species=species)
                    instance.pet_category.add(pet_category)
        if image_data is not None:
            for i, image in enumerate(image_data):
                Image.objects.update_or_create(id=image.get("id"), defaults={"image": image.get("image"), "order": i, "post": instance})

        instance.save()
        return instance

