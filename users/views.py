from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TinyUserSerializers

class My(APIView):  

    def get(self, request):
        user = request.user
        serializer = TinyUserSerializers(user)
        return Response(serializer.data)
    
    