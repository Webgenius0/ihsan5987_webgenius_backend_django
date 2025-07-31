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
    category = serializers.SerializerMethodField()  # change here

    class Meta:
        model = Post
        fields = [
            'id', 'user', 'title', 'category', 'image', 'content',
            'created_at', 'comment_count', 'commented_users'
        ]

    def get_comment_count(self, obj):
        # Use cached property if available, otherwise count
        if hasattr(obj, '_prefetched_objects_cache') and 'comments' in obj._prefetched_objects_cache:
            return len(obj._prefetched_objects_cache['comments'])
        return obj.comments.count()

    def get_commented_users(self, obj):
        # Use prefetched comments if available
        if hasattr(obj, '_prefetched_objects_cache') and 'comments' in obj._prefetched_objects_cache:
            comments = obj._prefetched_objects_cache['comments']
        else:
            comments = obj.comments.select_related('user__profile')
        
        users_dict = {}
        for comment in comments:
            users_dict[comment.user.id] = comment.user
        user_list = list(users_dict.values())[:5]
        return {
            'avatars': UserSerializer(user_list, many=True, context=self.context).data
        }

    def get_category(self, obj):
        if obj.category:
            return obj.category.category_name
        return None



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
        # Use cached property if available, otherwise count
        if hasattr(obj, '_prefetched_objects_cache') and 'likes' in obj._prefetched_objects_cache:
            return len(obj._prefetched_objects_cache['likes'])
        return obj.likes.count()

    def get_create_time(self, obj):
        diff = now() - obj.created_at
        if diff < timedelta(minutes=1):
            return "just now"
        return timesince(obj.created_at) + " ago"
    

class CommentReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentReport
        fields = ['id', 'comment', 'reason', 'message', 'status', 'created_at']
        read_only_fields = ['status', 'created_at', 'comment']


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