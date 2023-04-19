from django.urls import path
from . import views

urlpatterns=[
    path("", views.Posts.as_view()),
    path("<int:pk>", views.PostDetail.as_view()), 
    path("<int:pk>/comments", views.PostComments.as_view()),
    path("comments/", views.Comments.as_view()),
    path("comments/<int:pk>", views.CommentDetail.as_view()),
]