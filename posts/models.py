from django.db import models
from common.models import CommonModel


# 해야 할일 -> 다중이미지,
# 댓글 pageniation 최대 5개까지 보여주기
# 대댓글 3개

class Post(CommonModel):
    user=models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content=models.TextField(
        max_length=255,
        blank=True,
        null=True,
    )
    comments=models.ManyToManyField(
        "posts.Comment",
        blank=True,
        null=True,
        # on_delete=models.SET_NULL,
        related_name="posts",
    )
    pet_category=models.ManyToManyField(
        "pets.Pet",
        related_name="posts"
    )
    category=models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="posts",
    )
    def __str__(self):
        return f"{self.user} - {self.content}"
    
class Image(CommonModel):
    post=models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="images"
    )
    img_path=models.ImageField(
        upload_to="post_images", 
        blank=True, 
        null=True)
    
    #이미지 파일의 저장 경로를 받음
    #이미지파일의 주소 경로가 아님.
class Comment(CommonModel):
    user=models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE
    )    
    post=models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="post_comments",
    )
    content=models.CharField(#댓글 작성
        max_length=150,
        blank=True,
        null=True,
    )
    parent_comment=models.ForeignKey(#parent_comment에 값이 있으면 대댓글, 값이 없으면 댓글 
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="replies",
    )
    