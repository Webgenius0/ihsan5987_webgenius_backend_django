from django.contrib import admin
from unfold.admin import ModelAdmin   
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ("user", "title", "category", "image", "comment_count", "created_at")
    list_filter = ("category",)
    search_fields = ["user__email", "title"]
    ordering = ["-created_at"]

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ("post", "user", "text", "created_at")
    search_fields = ["post__title", "user__email"]
    ordering = ["-created_at"]

@admin.register(Like)
class LikeAdmin(ModelAdmin):
    list_display = ("comment", "user", "created_at")
    search_fields = ["comment__post__title", "user__email"]
    ordering = ["-created_at"]



