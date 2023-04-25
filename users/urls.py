from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns=[
    path("MY/Post", views.MyPost.as_view()),#user작성한 게시글 조회[GET]
    path("MY/Comment", views.MyComment.as_view()),#댓글 조회[GET]
    path("EditMe", views.EditMe.as_view()),# user profile 수정 [GET, PUT](ok) 
    path("getIP", views.getIP.as_view()),# user 현 위치의 동네 조회, 동네 설정[GET, POST] +)+)동네 재설정 추가, 동네 삭제[PUT]
    path("getQuery", views.getQuery.as_view()), # 검색어 기반 동네 조회 +) 검색어 기반 동네 검색, 동네 설정, 수정

    # path("resetRegion", views.ReSet.as_view()), #동네 재 설정 [GET, POST]
]