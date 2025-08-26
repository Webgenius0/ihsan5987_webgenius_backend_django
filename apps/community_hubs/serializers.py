from rest_framework import serializers
from django.utils.timesince import timesince
from django.utils.timezone import now
from datetime import timedelta
from apps.users.models import User
from .models import Post, Comment, Like, CommentReport, Category


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
        # Explicitly define read-only fields to avoid extra queries
        read_only_fields = ['id', 'created_at']

    # Optimize category serialization to avoid extra queries
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)

    def create(self, validated_data):
        # Explicitly handle user assignment to avoid extra queries
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


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
    user = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()  # ✅ use method field
    create_time = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'create_time', 'like_count', 'is_liked_by_user']

    def get_like_count(self, obj):
        # Use annotated like_count if available, else fallback
        if hasattr(obj, 'like_count'):
            return obj.like_count
        return obj.likes.filter(is_like=True).count()

    def get_user(self, obj):
        profile_image = ''
        if hasattr(obj.user, 'profile') and obj.user.profile.image:
            profile_image = str(obj.user.profile.image)
        return {
            'id': obj.user.id,
            'name': obj.user.name,
            'image': profile_image
        }

    def get_create_time(self, obj):
        diff = now() - obj.created_at
        if diff < timedelta(minutes=1):
            return "just now"
        return timesince(obj.created_at) + " ago"

    def get_is_liked_by_user(self, obj):
        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user, is_like=True).exists()
        return False


class CommentReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentReport
        fields = ['id', 'comment', 'reason', 'message', 'status', 'created_at']
        read_only_fields = ['status', 'created_at', 'comment']


class PostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    commented_users = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'image_url', 'title', 'category_name', 'content', 'created_at',
            'comment_count', 'commented_users', 'comments'
        ]

    def get_image_url(self, obj):
        if obj.image_url:
            return str(obj.image_url)  # convert CloudinaryResource to string
        return None

    def get_comments(self, obj):
        # use prefetched annotated comments
        comments = getattr(obj, 'prefetched_comments', obj.comments.all())
        serializer = CommentSerializer(comments, many=True, context=self.context)
        return serializer.data

    def get_comment_count(self, obj):
        return obj.comments.filter(is_active=True).count()

    def get_category_name(self, obj):
        if obj.category:
            return obj.category.category_name
        return None

    def get_commented_users(self, obj):
        # get unique users who commented
        comments = obj.comments.filter(is_active=True).select_related('user__profile')
        unique_users = {}
        for comment in comments:
            user = comment.user
            if user.id not in unique_users:
                profile_image = ''
                if hasattr(user, 'profile') and user.profile.image:
                    profile_image = str(user.profile.image)
                unique_users[user.id] = {
                    'id': user.id,
                    'name': user.name,
                    'image': profile_image
                }
        return {'avatars': list(unique_users.values())}
