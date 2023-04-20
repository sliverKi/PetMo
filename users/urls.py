from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns=[
    path("MY", views.My.as_view()),
    path("getIP", views.getIP.as_view()),
    path("getQuery", views.getQuery.as_view()),

]