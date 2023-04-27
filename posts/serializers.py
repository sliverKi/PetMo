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
from rest_framework.exceptions import ValidationError
import sys
from django.shortcuts import get_object_or_404
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
class ImageSerializers(ModelSerializer):
    # image=serializers.ImageField(use_url=True)
    class Meta:
        model=Image
        fields=(
            "img_path",
        )


class PostSerializers(ModelSerializer):
    pet_category=PetsSerializers(many=True, read_only=True)
    user=TinyUserSerializers(read_only=True)
    images=ImageSerializers(many=True, read_only=True, required=False)
    # uploaded_img=serializers.ListField(
    #     child=serializers.ImageField(
    #     max_length=1000000,
    #     allow_empty_file=False,
    #     use_url=False,), 
    #     write_only=True,
    #     required=False
    # )
    #images=serializers.SerializerMethodField()#required=False : 필수 필드가 아닌 선택 필드로 지정 

    class Meta:
        model=Post
        fields=(
            "pk",
            "user",
            "content",
            # "images",#ImageModel의 post field의 relatedname 이용 
            # "uploaded_img",
            "images",
            "category",
            "pet_category",
            
        )
    def create(self, validated_data):  
        pet_category_data=validated_data.pop("pet_category", None)
        uploaded_img = validated_data.pop("upload_image", None)#값 없으면 None
        try:
            with transaction.atomic():
                post = Post.objects.create(**validated_data)
            
                if uploaded_img:
                    Image.objects.create(post=post, img_path=uploaded_img)
                    # for image in uploaded_img:
                if pet_category_data:
                    if isinstance(pet_category_data, list):
                        for pet_category in pet_category_data:
                            category = get_object_or_404(Pet,species=pet_category)
                            post.pet_category.add(category)
                    else:
                        category = get_object_or_404(Pet,species=pet_category_data)
                        post.pet_category.add(category)
                else:
                    raise ParseError(1)
        except Exception as e:
            print(e)
            raise ValidationError({"error":str(e)})
        return post
        
    def validate(self, data):
        content = data.get('content', None)
        images = data.get('images', None)
        if content is None and images is None:
            raise ParseError({"error": "내용을 입력해주세요."})
        if images and len(images)>5:
            raise ParseError({"error":"이미지는 최대 5개까지 등록이 가능합니다."})
        return data
    


class PostListSerializers(ModelSerializer):#간략한 정보만을 보여줌
    user=TinyUserSerializers(read_only=True)
    pet_category=PetsSerializers(many=True)
    category=BoardSerializers()
    images=ImageSerializers(many=True, required=False)#첫번째 이미지만 보여줌 

    class Meta:
        model=Post
        fields=(
            "pk",
            "category",
            "pet_category",
            "user",
            "content",
            "images",
            "created_at", 
            "updated_at",
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
    images=ImageSerializers(many=True)
    
    class Meta:
        model=Post
        fields=(
            "id",
            "category",
            "pet_category",
            "user", 
            "content",
            "images",
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

