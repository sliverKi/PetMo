from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Bookmark
from .serializers import  BookmarkSerializers

from posts.models import Post, Comment
from posts.serializers import PostDetailSerializers, ReplySerializers
class Bookmarks(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound
        
    def get(self, request):
        all_bookmarks=Bookmark.objects.filter(user=request.user)
        serializer = BookmarkSerializers(
            all_bookmarks,
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        #input data : {"post":3}
        post=self.get_object(request.data.get("post"))
        serializer=BookmarkSerializers(data=request.data)
        if serializer.is_valid():
            if Bookmark.objects.filter(
                user=request.user,
                post=post
            ).exists():
                Bookmark.objects.filter(
                    user=request.user,
                    post=post
                ).delete()    
                return Response({"ok":"delete success"}, status=status.HTTP_202_ACCEPTED)
            
            else:
                bookmark=serializer.save(
                user=request.user,
                post=post
            )
            serializer=BookmarkSerializers(bookmark)
            return Response({"ok": "create success"}, status=status.HTTP_201_CREATED)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MarkDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        post=self.get_object(pk)
        post_serializer = PostDetailSerializers(
            post,
            context={"request":request},
        )
        comments = Comment.objects.filter(parent_comment=None)
        comments_serializer=ReplySerializers(
            comments,
            many=True,
        )
        return Response(
            {
                "post":post_serializer.data,
                "comments":comments_serializer.data
            },
            status=status.HTTP_200_OK
        )
    


        

