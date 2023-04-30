from django.urls import path
from . import views

urlpatterns=[
    path("", views.Bookmarks.as_view()),
]