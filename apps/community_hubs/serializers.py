from rest_framework import serializers
from apps.users.models import User
from django.utils.timesince import timesince
from django.utils.timezone import now
from datetime import timedelta
from apps.profiles.models import Profile
from apps.users.models import User
from .models import Post, Comment, Like, CommentReport

class PostlistSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    commented_users = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'content', 'created_at', 'comment_count', 'commented_users']

    def get_commented_users(self, obj):
        # Get the list of users who have commented on this post
        comments = obj.comments.filter(post=obj).select_related('user__profile')
        users = {comments.user.id: comments.user for comments in comments}.values()
    
        # Limit to 5 for avatars (you can make this dynamic or full list based on your UI)
        max_users = 5
        user_list = list(users)[:max_users]
        # overflow = len(users) - max_users if len(users) > max_users else 0
        
        return {
            'avatars': UserSerializer(user_list, many=True, context=self.context).data,
            # 'overflow': overflow
        }

    def get_comment_count(self, obj):
        return obj.comment_count()


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'image', 'title', 'category', 'content', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'image']

    def get_image(self, obj):
        if hasattr(obj, 'profile') and obj.profile.image:
            return obj.profile.image.url
        return None



class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'create_time', 'like_count',]

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_create_time(self, obj):
        diff = now() - obj.created_at
        if diff < timedelta(minutes=1):
            return "just now"
        return timesince(obj.created_at) + " ago"
    

class CommentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReport
        fields = ['id', 'reason', 'message', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['image_url', 'title', 'content', 'comments']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Reorder fields to match requested structure: image, title, content, then comments
        ordered_data = {
            'image': representation['image_url'],
            'title': representation['title'],
            'content': representation['content'],
            'comments': representation['comments'],
        }
        return ordered_data
    