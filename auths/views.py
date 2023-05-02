from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from config.settings import KAKAO_API_KEY
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.permissions import AllowAny
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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
           return Response({"error":"이메일과비밀번호를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        user=authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            serializer=UserSerializers(user)
        
            
            token = {
                # "refresh": str(refresh),
                # "access": str(refresh.access_token),#access token 생성
                # "user_id":user.id,
                # "user_email":user.email,
                # "username":user.username,
                "user":serializer.data,
            } 

            return Response(token, status=status.HTTP_200_OK)
        #  if user is not None:
        #     login(request, user)
        #     serializer=UserSerializers(user)
        #     # refresh=self.get_token(self.user)
        #     refresh=RefreshToken.for_user(user)
            
        #     refresh_token: str(refresh)
        #     access_token: str(refresh.access_token)#access token 생성
        #     # request.session["refresh_token"]=refresh_token
        #     # request.session["access_token"]=access_token
            
        #     res = Response({
        #         "user":serializer.data,
        #         "success":"Login Success!",
        #     }, status=status.HTTP_200_OK)
        #     return Response(res)
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

class KakaoException(Exception):
    pass

class KakaoLogin(APIView):
    def get(self, request):
        kakao_api="https://kauth.kakao.com/oauth/authorize?response_type=code"
        redirect_uri="http://127.0.0.1:8000/api/v1/auths/kakao/callback"
        client_id=KAKAO_API_KEY
        return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")

class KakaoCallBack(APIView):
    def get(self, request):
        try:
            code = request.GET.get("code")
            client_id = KAKAO_API_KEY
            redirect_uri = "http://127.0.0.1:8000/api/v1/auths/kakao/callback"
            token_request = requests.post(
                "https://kauth.kakao.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": client_id,
                    "redirect_uri": redirect_uri,
                    "code": code,
               },
            )
            token_json = token_request.json()
            print(token_json)
            
            error = token_json.get("error", None)
            
            if error is not None:
                return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)
            
            access_token = token_json.get("access_token")
            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    # "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                },
            )
            profile_json = profile_request.json()
            # print(profile_request)
            kakao_account =profile_json.get("kakao_account")
            # print(kakao_account)
            
            if email is None:
                raise KakaoException()
            email = kakao_account.get("email", None)#왜 None?
            nickname = kakao_account.get("profile", None).get("nickname", None)
            
        except KeyError:
            return Response({"message": "INVALID_TOKEN"}, status=status.HTTP_400_BAD_REQUEST)
        
        # except access_token.DoesNotExist:
        #     return Response({"message": "INVALID_TOKEN"}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            kakao_user = User.objects.get(email=email)
            refresh=RefreshToken.for_user(kakao_user)
            response=HttpResponseRedirect(
                # front 주소 
                # f"http://127.0.0.1:8000/KakaoLogin?refresh={str(refresh)}&access={str(refresh.access_token)}"

            )
            print("success")
            return Response(response, status=status.HTTP_200_OK)
            
        else:
            if email:
                user=User.objects.create(
                    email=email, username=nickname,
                )
                refresh = RefreshToken.for_user(user)
                response=HttpResponseRedirect(
                    # f"http://127.0.0.1:8000/KakaoLogin?refresh={str(refresh)}&access={str(refresh.access_token)}"
                    
                )
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error":"MISSING ACCOUNT"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

class NaverLogin(APIView):    
    def post(self, request):
        code = request.data.get("code")
        state = request.data.get("state")
        
        access_token = (
            requests.post(
                "https://nid.naver.com/oauth2.0/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": "kq20IeckeIhaC1BsAKuF",
                    "client_secret": "4FTGMSzqCd",
                    "code": code,
                    "state": state,
                },
            )
            .json()
            .get("access_token")
        )
        user_data = requests.get(
            "https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {access_token}"},
        ).json()
        if (
            user_data.get("resultcode") == "00"
            and user_data.get("message") == "success"
        ):
            response = user_data.get("response")
            try:
                user = User.objects.get(email=response.get("email"))
                login(request, user)
                return Response(status=200)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=response.get("id")[:10],
                    name=response.get("name"),
                    phone_number=response.get("mobile").replace("-", ""),
                    email=response.get("email"),
                    gender="male" if response.get("gender") == "M" else "female",
                    avatar=response.get("profile_image"),
                    is_naver=True,
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response(
                    {"access": str(refresh.access_token), "refresh": str(refresh)},
                    status=201,
                )

        return Response(status=400)

