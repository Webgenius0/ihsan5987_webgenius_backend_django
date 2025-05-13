from django.urls import path
from .views import PostList, CreatePost, PostDetail

urlpatterns = [
    path('posts/', PostList.as_view(), name='all-posts'),
    path('posts/create/', CreatePost.as_view(), name='create-post'),
    path('posts/<int:post_id>/', PostDetail.as_view(), name='post-detail'),
]
