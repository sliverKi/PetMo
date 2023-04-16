from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from categories.serializers import BoardSerializers
from pets.serializers import PetsSerializers

from .models import Post,Comment
from .serializers import PostListSerializers, PostDetailSerializers, CommentSerializers


class Comments(APIView):
    def get(self,request):
        all_comments=Comment.objects.all()
        serializer=CommentSerializers(all_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Posts(APIView):
    def get(self, request):
        all_posts=Post.objects.all()
        serializer=PostListSerializers(all_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        pass

class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound

    def get(self,request,pk):
        post=self.get_object(pk)
        serializer = PostDetailSerializers(
            post,
            context={"request":request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
        
