from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q, Count
from .models import Post
from .serializers import PostlistSerializer,CreatePostSerializer, PostDetailSerializer


class PostList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        sort = request.GET.get("sort", "latest")
        search = request.GET.get("search")

        posts = Post.objects.all()

        if search:
            posts = posts.filter(Q(title__icontains=search) | Q(category__icontains=search))

        if sort == "most_commented":
            posts = posts.annotate(num_comments=Count("comments")).order_by("-num_comments")
        elif sort == "most_interested":
            posts = posts.annotate(num_comments=Count("comments")).order_by("-num_comments")
        else:
            posts = posts.order_by("-created_at")  # latest

        serializer = PostlistSerializer(posts, many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Posts fetched successfully",
            "data": serializer.data
        })

class CreatePost(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CreatePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Post created successfully",
                "post_id": serializer.data['id']
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Post creation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class PostDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Post not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = PostDetailSerializer(post)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Post details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)