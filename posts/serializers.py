from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.response import Response
from rest_framework import status


from users.serializers import TinyUserSerializers
from .models import Post,Comment
from images.models import Image
from images.serializers import ImageSerializers
from categories.models import Category
from categories.serializers import BoardSerializers
from pets.models import Pet
from pets.serializers import PetsSerializers
import sys

from django.db import transaction
sys.setrecursionlimit(100000)


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
    category=BoardSerializers(many=True, read_only=True)
    pet_category=PetsSerializers(many=True, read_only=True)
    user=TinyUserSerializers(read_only=True)
    Image=ImageSerializers(many=True, read_only=True, required=False)
   
    class Meta:
        model=Post
        fields=(
            "pk",
            "category",
            "pet_category",
            "user",
            "content",
            "Image",#ImageModel의 relatedname 이용 
        )

    def create(self, validated_data):  
        #input data: {"content":"test post", "pet_category":["cat"], "Image":[], "category":"Review"}        
        category_data=validated_data.pop("category", None)
        pet_category_data=validated_data.pop("pet_category", None)
        image_data = validated_data.pop("Image", None)#값 없으면 None
        try:
            with transaction.atomic():
                post = Post.objects.create(**validated_data)
                if category_data:
                    for i in Category.objects.all():
                        print(i.type)
                    category=Category.objects.filter(type=category_data).first()
                    post.category=category
                    post.save()

                if image_data:
                    if isinstance(image_data, list):
                        if len(image_data)<=5:
                            for img in image_data:
                                Image.objects.create(post=post, img_path=img.get("img_path"))
                        else:
                            raise ParseError("이미지는 최대 5장 까지 업로드 할 수 있습니다.") 
                    else:
                        raise ParseError("image 잘못된 형식 입니다.")               

                if pet_category_data:
                    if isinstance(pet_category_data, list):
                        for pet_category in pet_category_data:
                            pet_category = get_object_or_404(Pet,species=pet_category)
                            post.pet_category.add(pet_category)
                    else:
                        pet_category = get_object_or_404(Pet, species=pet_category_data)
                        post.pet_category.add(pet_category)
                else:
                    raise ParseError({"error": "잘못된 형식입니다."})
        
        except Exception as e:
            raise ValidationError({"error":str(e)})
        return post
        
    def validate(self, data):
        content = data.get('content', None)
        images = data.get('Image', None)
        if content is None and images is None:
            raise ParseError({"error": "내용을 입력해주세요."})
        if images and len(images)>5:
            raise ParseError({"error":"이미지는 최대 5개까지 등록이 가능합니다."})
        return data

class PostListSerializers(ModelSerializer):#간략한 정보만을 보여줌
    user=TinyUserSerializers(read_only=True)
    pet_category=PetsSerializers(many=True)
    category=BoardSerializers()
    Image=ImageSerializers(many=True, read_only=True, required=False)

    class Meta:
        model=Post
        fields=(
            "pk",
            "category",
            "pet_category",
            "user",
            "content",
            "Image",
            "created_at", 
            "updated_at",
            "watcher",
        )
    def get_images(self, post):
        images = post.images.all()
        if images.exist():
            return ImageSerializers(images.first(), context=self.context).data   
        return [] 
class PostDetailSerializers(ModelSerializer):#image 나열
    user=TinyUserSerializers()
    pet_category=PetsSerializers(many=True)
    category=BoardSerializers()
    Image=ImageSerializers(many=True, read_only=True, required=False)

    
    class Meta:
        model=Post
        fields=(
            "id",
            "category",
            "pet_category",
            "user", 
            "content",
            "Image",
            "created_at",
            "updated_at",    
            "watcher",
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
        # image_data = validated_data.pop("Image", None)
        category_data = validated_data.pop("category", None)
        
        if category_data is not None:
            category_instance = Category.objects.filter(type=category_data).first()
            # print("a: ", category_instance)
            if category_instance is None:
                raise serializers.ValidationError({"category": "Invalid category"})
            instance.category = category_instance

        # Update the remaining fields
        instance = super().update(instance, validated_data)

        # Update the many-to-many fields
        if pet_category_data:
            if isinstance(pet_category_data,list):
                for pet_category in pet_category_data:
                    pet_category = get_object_or_404(Pet,species=pet_category)
                    instance.pet_category.add(pet_category)
                
            else:
                pet_category, _ = Pet.objects.get_or_create(species=pet_category)
                instance.pet_category.add(pet_category)

        instance.save()
        return instance
  