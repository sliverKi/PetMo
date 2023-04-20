from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.permissions import AllowAny
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework.exceptions import NotFound, ParseError

from users.models import User
# from users.serializers import UserSerializers

class LogIn(APIView):
    def post(slef, request, format=None):
        email=request.data.get('email')
        password=request.data.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound
        
        if not email or not password:
            raise ParseError("잘못된 정보를 입력하셨습니디.")
        
        user=authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            refresh=RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return Response({"token":token}, status=status.HTTP_200_OK)
            #return Response(token, status=status.HTTP_200_OK)::front 전달
        else:
            return Response({"error":"Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogOut(APIView):
    def post(self, request):
        token=request.data.get("token")
        try:
            AccessToken(token).blacklist()#token무효화 
            logout(request)
            return Response({"success":"Success LogOut!"}, status=status.HTTP_200_OK)
        except:
            return Response({"error":"LogOut Failed..."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
class Register(APIView):
    pass
#     def post(self, request):

