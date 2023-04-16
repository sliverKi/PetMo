from django.db import models
from common.models import CommonModel

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
    image=models.URLField(
        max_length=500,
        blank=True,
        null=True,
    )
    comments=models.ManyToManyField(
        "posts.Comment",
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
    )
    content=models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    parent_comment=models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )#parent_comment에 값이 있으면 대댓글, 값이 없으면 댓글 