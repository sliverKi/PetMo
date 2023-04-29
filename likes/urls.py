
from django.urls import path
from . import views

urlpatterns=[
    path("postlike/<int:pk>", views.PostLikes.as_view()),
    # path("commentlike/<int:pk>", views.CommentLikes.as_view()),
]