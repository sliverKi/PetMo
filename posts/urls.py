from django.urls import path
from . import views

urlpatterns=[
    path("", views.Posts.as_view()),#[GET,POST]
    path("<int:pk>", views.PostDetail.as_view()),#[GET, PUT(게시글 수정), DELETE]
    path("<int:pk>/comments", views.PostComments.as_view()),#[GET, POST(댓글,대댓글 등록가능)]
    path("<int:pk>/comments/<int:comment_pk>", views.PostCommentsDetail.as_view()), #[GET, PUT(댓글 대댓글 수정, DELETE]
    path("comments/", views.Comments.as_view()), #[GET, POST]
    path("comments/<int:pk>", views.CommentDetail.as_view()),#[GET,PUT,DELETE]
]