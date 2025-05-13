from rest_framework import serializers
from .models import Post, Comment, Like
from apps.users.models import User
from django.utils.timesince import timesince
from django.utils.timezone import now
from datetime import timedelta

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
        fields = ['id', 'title', 'category', 'content', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['name', 'image']

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
        fields = ['user', 'text', 'create_time', 'like_count',]

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_create_time(self, obj):
        diff = now() - obj.created_at
        if diff < timedelta(minutes=1):
            return "just now"
        return timesince(obj.created_at) + " ago"


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['image', 'title', 'content', 'comments']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Reorder fields to match requested structure: image, title, content, then comments
        ordered_data = {
            'image': representation['image'],
            'title': representation['title'],
            'content': representation['content'],
            'comments': representation['comments'],
        }
        return ordered_data