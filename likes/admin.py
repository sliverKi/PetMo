from django.contrib import admin
from .models import PostLike, CommentLike

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display=("id", "user", "post")

@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display=("id", "user", "comment")
