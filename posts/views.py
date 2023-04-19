from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from categories.serializers import BoardSerializers
from pets.serializers import PetsSerializers

from .models import Post,Comment
from .serializers import (
    PostSerializers,
    PostListSerializers, PostDetailSerializers, 
    CommentSerializers, CommentDetailSerializers,
    ReplySerializers
    )


        


class Comments(APIView):
    #예외 : 존재 하지 않는 게시글에 댓글 작성 불가
    #예외 : 존재 하지 않는 게시글에 대댓글 작성 불가
    #에외 : 존재 하지 않는 댓글에 대댓글 작성 불가
    def get(self,request):
        all_comments=Comment.objects.filter(parent_comment=None)
        serializer=ReplySerializers(all_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        
        content=request.data.get("content")
        post_id=request.data.get("post")
        parent_comment_id = request.data.get("parent_comment", None)
        #부모댓글 정보 
        #부모댓글 정보가 전달 되지 않을 경우, None할당(=댓글)
        
        try:
            post=Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error":"해당 게시글이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        if parent_comment_id is not None:##대댓글
            try:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                print(parent_comment)
            except Comment.DoesNotExist:
                return Response({"error":"해당 댓글이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
            print("대댓글 작성1")
            comment=Comment.objects.create(
            content=content,
            user=request.user,
            post=parent_comment.post,
            parent_comment=parent_comment
            )
            serializer = ReplySerializers(comment)
            print("대댓글 작성2")
            return Response(serializer.data, status=status.HTTP_201_CREATED)           
        else: #댓글
            print("댓글")
            serializer=CommentSerializers(data=request.data)
            if serializer.is_valid():
                comment=serializer.save(post=post)
                serializer=CommentSerializers(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            

     
class CommentDetail(APIView):# 댓글:  조회 생성, 수정, 삭제(ok)
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        # if comment_id = 1이면 parent_comment_id가 1인 아이들도 가져 와야 함.~>filter()
        comment=self.get_object(pk=pk)
        serializer=ReplySerializers(
            comment,
            context={"request":request},                                    
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request,pk): 
        # 댓글과 대댓글의 수정은 독립적으로 이루어져야 함.
        comment=self.get_object(pk=pk)
        serializer=CommentDetailSerializers(
            comment, 
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            updated_comment=serializer.save()
            return Response(CommentSerializers(updated_comment).data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):
        #예외 : 댓글응 삭제할떄 post도 검사해야 함.
        comment=self.get_object(pk)
        
        if comment.user!=request.user:
            raise PermissionDenied
        comment.delete()
        return Response(status=status.HTTP_200_OK)

                     
class Posts(APIView):
    def get(self, request):
        all_posts=Post.objects.all()
        serializer=PostListSerializers(all_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        #예외 : image field, content field 둘 중 하나는 값이 있어야 함. 
        serializer=PostSerializers(data=request.data)

        if serializer.is_valid():    
            post=serializer.save(
                user=request.user
            )
            serializer=PostListSerializers(
                post,
                context={'request': request}, 
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

    

class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound

    def get(self,request,pk):
        post=self.get_object(pk)
        print(post.comments)
        serializer = PostDetailSerializers(
            post,
            context={"request":request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class PostComments(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound

    def get(slef, request, pk):
        comments=Comment.objects.filter(parent_comment=None)
        serializer=ReplySerializers(
            comments, 
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
