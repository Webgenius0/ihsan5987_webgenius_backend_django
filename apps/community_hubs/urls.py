from django.urls import path
from .views import (
    PostList,
    CreatePost,
    PostDetail,
    CommentView,
    LikeView,
    CommentReportView
)

urlpatterns = [
    path('posts/', PostList.as_view(), name='all-posts'),
    path('posts/create/', CreatePost.as_view(), name='create-post'),
    path('posts/<int:post_id>/', PostDetail.as_view(), name='post-detail'),
    path("post/<int:post_id>/comments/", CommentView.as_view(), name="comment-list"),
    path("comment/", CommentView.as_view(), name="comment-create"),
    path("comment/<int:pk>/", CommentView.as_view(), name="comment-edit-delete"),
    path("comment/like/<int:pk>/", LikeView.as_view(), name="like-toggle"),
    path('comment/<int:pk>/report/', CommentReportView.as_view(), name='report-comment'),
]
