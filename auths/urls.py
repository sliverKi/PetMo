from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views 

urlpatterns=[
    path("sign-up", views.Register.as_view()),
    path("sign-in", views.LogIn.as_view()),
    path("sign-out", views.LogOut.as_view()),
    # path("sign-in/refresh", views.RefreshTocken.as_view()),
]