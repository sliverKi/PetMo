from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views 

urlpatterns=[
    path("sign-up", views.Register.as_view()),
    path("sign-in", views.LogIn.as_view(), name="get_token"),
    path("sign-in/refresh", views.TokenBlack.as_view(), name="get_newToken"),
    path("sign-out", views.LogOut.as_view()),

    path("kakao", views.KakaoLogin.as_view()),
]