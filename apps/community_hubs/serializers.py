from rest_framework import serializers
from .models import Post, Comment, Like
from apps.users.models import User
from django.utils.timesince import timesince
from django.utils.timezone import now
from datetime import timedelta
from apps.profiles.models import Profile

class PostlistSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'content', 'created_at', 'comment_count']

    def get_comment_count(self, obj):
        return obj.comment_count()


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'image', 'title', 'category', 'content', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', required=False)
    class Meta:
        model = Profile
        fields = ['name', 'image_url']


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['user', 'created_at']

class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'profile_image']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user.profile', read_only=True)
    like_count = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['user', 'text', 'create_time', 'like_count',]

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_create_time(self, obj):
        diff = now() - obj.created_at
        if diff < timedelta(minutes=1):
            return "just now"
        return timesince(obj.created_at) + " ago"


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