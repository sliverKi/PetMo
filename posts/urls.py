from django.urls import path
from . import views

urlpatterns=[
    path("", views.Posts.as_view()),#[GET,POST]
    path("<int:pk>", views.PostDetail.as_view()),#[GET, POST(댓글 등록 가능), PUT(게시글 수정만 가능, 댓글도 수정할 수 있게 만들것 ), DELETE]
    # path("<int:pk>/modified", views.modifiedPostDetail.as_view()),
    path("<int:pk>/comments", views.PostComments.as_view()),#[GET, POST(댓글,대댓글 등록가능)]
    # path("<int:pk>/comments/<int:comment_pk>", views.PostCommentsDetail.as_view()), #할일 [GET, PUT, DELETE]
   
    path("comments/", views.Comments.as_view()), #[GET, POST]
    path("comments/<int:pk>", views.CommentDetail.as_view()),#[GET,PUT,DELETE]
]