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
from users.serializers import UserSerializers

import requests
class LogIn(APIView):
    def post(self, request, format=None):
        email=request.data.get('email')
        password=request.data.get('password')
        
        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            raise NotFound
        
        if not email or not password:
            raise ParseError("잘못된 정보를 입력하셨습니다.")
        
        user=authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            # refresh=self.get_token(self.user)
            refresh=RefreshToken.for_user(user)
            token = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),#access token 생성
                "user_id":user.id,
                "user_email":user.email,
                "username":user.username,
            } 
            return Response(token, status=status.HTTP_200_OK)
            #return Response(token, status=status.HTTP_200_OK)::front 전달
        else:
            return Response({"error":"Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
class TokenBlack(APIView):
    def post(self, request):
       
        refresh_token=request.data.get("refresh")
        print("refresh_token: ", refresh_token)
        if refresh_token:
            print("111")
            try:
                token=RefreshToken(refresh_token)
                print("token: ", token)
                token.blacklist()#이전 refresh token 무효화 

                user_id=token.payload["user_id"]
                user=User.objects.get(id=user_id)
                print("user: ", user)

                new_token=RefreshToken.for_user(user)
                print("new_token: ", new_token)
                response = {
                    "refresh": str(new_token),
                    "access": str(new_token.access_token),
                }
                return Response(response, status=status.HTTP_200_OK)
            except:
                return Response({'error': 'Token not found.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Refresh token is not provided.'}, status=status.HTTP_400_BAD_REQUEST)
       
# {"email":"momo@gmail.com", "password":"momo"}

class LogOut(APIView):
    def post(self, request):
        refresh_token=request.data.get("refresh")
        print("refresh_token: ", refresh_token)
        try:
            print(request.auth)
            token = RefreshToken(refresh_token)
            print("token: ", token)
            print(dir(token))
            token.blacklist()#token을 무효화 주석해제하면 로그아웃이 안됌,, =>>> 왜지???
            logout(request)
            return Response({"success":"Success LogOut!"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error":"LogOut Failed..."}, status=status.HTTP_406_NOT_ACCEPTABLE)        
class Register(APIView):
    def post(self, request, format=None):
        serializer=UserSerializers(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            refresh=RefreshToken.for_user(user)
            token=str(refresh.access_token)
            return Response({"token": token}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KakaoLogin(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = (
                requests.post(
                    "https://kauth.kakao.com/oauth/token",
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    data={
                        "grant_type": "authorization_code",
                        "client_id": "da7b6b984fe482fd404d22bff8e2f803",
                        "redirect_uri": "http://127.0.0.1:3000/social/kakao",
                        "code": code,
                    },
                )
                .json()
                .get("access_token")
            )
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                },
            ).json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(email=kakao_account.get("email"))
                login(request, user)
                return Response(status=200)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=kakao_account.get("email"),
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
            user.set_unusable_password()
            user.save()
            login(request, user)
            return Response(status=200)
        except Exception:
            return Response(status=400)