from django.urls import path
from .views import ProfileView, MyPostList, MyPostDetail

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('my-posts/', MyPostList.as_view(), name='my-posts'),
    path('my-posts/<int:pk>/', MyPostDetail.as_view(), name='my-post-detail'),
]