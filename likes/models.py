from django.db import models
from common.models import CommonModel


class PostLike(CommonModel):
    user=models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE
    )
    post=models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        related_name="postlike"
    )
    unique_together=("user", "post")

class CommentLike(CommonModel):
    user=models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE
    )
    comment=models.ForeignKey(
        "posts.Comment",
        on_delete=models.CASCADE,
        blank=True, 
        null=True,
        related_name="commentlike"
    )
    unique_together=("user", "comment")
    
