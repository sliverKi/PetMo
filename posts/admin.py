from django.contrib import admin
from .models import Post,Comment
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=("category", "user", "content")
    list_display_links=("user", "content")

    search_fields=("category","pet_category", "user",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=("id","user","post","content",)
    list_display_links=("id","user","post","content",)
    search_fields=("user",)
