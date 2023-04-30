from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Bookmark
from .serializers import  BookmarkSerializers

class Bookmarks(APIView):
    def get(self, request):
        all_bookmarks=Bookmark.objects.filter(user=request.user)
        serializer = BookmarkSerializers(
            all_bookmarks,
            many=True,
            context={"request":request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        #input data : {"post":3}
        serializer=BookmarkSerializers(data=request.data)
        if serializer.is_valid():
            bookmark=serializer.save(
                user=request.user,
            )
            serializer=BookmarkSerializers(bookmark)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

