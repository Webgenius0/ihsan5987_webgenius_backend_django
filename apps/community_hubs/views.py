from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status, permissions
from django.db.models import Q, Count, Prefetch
from auditlog.registry import auditlog
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like, CommentReport
from .serializers import (
    PostlistSerializer,
    CreatePostSerializer,
    PostDetailSerializer,
    CommentSerializer,
    LikeSerializer,
    CommentReportSerializer
)


class PostList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        sort = request.GET.get("sort", "latest")
        search = request.GET.get("search")

        posts = Post.objects.select_related(
            'user__profile', 'category').prefetch_related(
            'comments__user__profile', 'comments__likes'
        )

        if search:
            posts = posts.filter(Q(title__icontains=search) | Q(category__category_name__icontains=search))

        if sort == "most_commented":
            posts = posts.annotate(
                num_comments=Count("comments")
            ).order_by("-num_comments")
        elif sort == "most_interested":
            posts = posts.annotate(
                num_comments=Count("comments")
            ).order_by("-num_comments")
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
        # Pass request context to serializer to avoid redundant user queries
        serializer = CreatePostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            post = serializer.save()  # User is set in serializer's create method
            return Response({
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Post created successfully",
                "post_id": post.id
            }, status=status.HTTP_201_CREATED)

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
            comments_qs = Comment.objects.filter(is_active=True).select_related(
                'user__profile'
            ).annotate(
                like_count=Count('likes', filter=Q(likes__is_like=True))
            ).order_by('-created_at')

            post = Post.objects.select_related('user__profile', 'category').prefetch_related(
                Prefetch('comments', queryset=comments_qs, to_attr='prefetched_comments')
            ).get(id=post_id)

        except Post.DoesNotExist:
            return Response({
                "status": 404,
                "success": False,
                "message": "Post not found"
            }, status=404)

        serializer = PostDetailSerializer(post, context={'request': request})
        return Response({
            "status": 200,
            "success": True,
            "message": "Post retrieved successfully",
            "data": serializer.data
        })

    def delete(self, request, post_id):
        post = Post.objects.filter(id=post_id, user=request.user).first()
        if not post:
            return Response({
                "status": status.HTTP_403_FORBIDDEN,
                "success": False,
                "message": "You do not have permission to delete this post"
            }, status=status.HTTP_403_FORBIDDEN)

        # Bulk delete related objects to avoid N+1 queries
        CommentReport.objects.only('id').filter(comment__post=post).delete()
        Like.objects.only('id').filter(comment__post=post).delete()
        Comment.objects.only('id').filter(post=post).delete()
        post.delete()

        return Response({
            "status": status.HTTP_204_NO_CONTENT,
            "success": True,
            "message": "Post deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_id):
        comments = Comment.objects.filter(
            post_id=post_id, is_active=True
        ).select_related(
            'user__profile'
        ).prefetch_related(
            'likes'
        ).annotate(
            like_count=Count('likes', filter=Q(likes__is_like=True))  # ✅ only count likes
        ).order_by("-created_at")

        serializer = CommentSerializer(comments, many=True, context={'request': request})
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

        serializer = CommentSerializer(comment)
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
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Comment deleted successfully"
        }, status=status.HTTP_200_OK)


class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        like, created = Like.objects.get_or_create(
            user=request.user,
            comment=comment,
            defaults={"is_like": True}
        )

        if not created and like.is_like:
            # User already liked → toggle off
            like.is_like = False
            like.save()
            return Response({
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Like removed successfully"
            }, status=status.HTTP_200_OK)

        else:
            # New like OR previously unliked → like again
            like.is_like = True
            like.save()
            serializer = LikeSerializer(like)
            return Response({
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Comment liked successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)


class CommentReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "Comment not found"
            }, status=status.HTTP_404_NOT_FOUND)

        if CommentReport.objects.filter(comment=comment, reporter=request.user).exists():
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "You have already reported this comment"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(comment=comment, reporter=request.user)

            # Send email notification to admin
            send_mail(
                subject='🚨 New Comment Report',
                message=f"A new comment has been reported:\n\nComment ID: {comment.id}\nReason: {serializer.validated_data['reason']}\nMessage: {serializer.validated_data.get('message', 'No message provided')}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            return Response({
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Comment reported successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Failed to report comment",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def save(self, *args, **kwargs):
        if self.pk:
            previous = CommentReport.objects.get(pk=self.pk)
            if previous.status != 'dismissed' and self.status == 'dismissed':
                self.comment.is_active = False
                self.comment.save()

        elif self.status == 'dismissed':
            self.comment.is_active = False
            self.comment.save()

        super().save(*args, **kwargs)
