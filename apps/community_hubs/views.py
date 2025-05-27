from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostlistSerializer,CreatePostSerializer, PostDetailSerializer, CommentSerializer, LikeSerializer


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
    

class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id).order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Comments fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        text = request.data.get("text")
        post_id = request.data.get("post")

        if not text or not post_id:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Text and post ID are required"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        comment = Comment.objects.create(
            post_id=post_id,
            user=request.user,
            text=text
        )
        serializer = CommentSerializer(comment)
        response = {
            "status": status.HTTP_201_CREATED,
            "success": True,
            "message": "Comment created successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.user != request.user:
            return Response({
                "status": status.HTTP_403_FORBIDDEN,
                "success": False,
                "message": "You do not have permission to edit this comment"
            }, status=status.HTTP_403_FORBIDDEN)
        
        new_text = request.data.get("text")
        if not new_text:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Text is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        comment.text = new_text
        comment.save()

        serializer =  CommentSerializer(comment)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Comment updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.user != request.user:
            return Response({
                "status": status.HTTP_403_FORBIDDEN,
                "success": False,
                "message": "You do not have permission to delete this comment"
            }, status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return Response({
            "status": status.HTTP_204_NO_CONTENT,
            "success": True,
            "message": "Comment deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        comment_id = request.data.get("comment")

        if not comment_id:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Comment id is required"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        comment = get_object_or_404(Comment, id=comment_id)

        like_qs = Like.objects.filter(user=request.user, comment=comment)

        if like_qs.exists():
            like_qs.delete()
            return Response({
                "status": status.HTTP_204_NO_CONTENT,
                "success": True,
                "message": "Like removed successfully"
            }, status=status.HTTP_204_NO_CONTENT)
        
        else:
            like = Like.objects.create(user=request.user, comment=comment)
            serializer = LikeSerializer(like)
            return Response({
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Comment liked successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)