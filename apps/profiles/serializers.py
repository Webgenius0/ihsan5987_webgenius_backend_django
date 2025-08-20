from rest_framework import serializers
from apps.community_hubs.models import Post
from apps.community_hubs.serializers import UserSerializer, CommentSerializer
from .models import Profile, FAQ, FAQCategory, ContactUs, NotificationSetting, AppInfo


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['image', 'name']  # name is now part of the serializer

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['email'] = instance.user.email
        data['id'] = instance.user.id
        return data

    def update(self, instance, validated_data):
        # Update related user.name if provided
        user_data = validated_data.pop('user', {})
        name = user_data.get('name')
        if name:
            instance.user.name = name
            instance.user.save()

        # Update profile image if provided
        image = validated_data.get('image')
        if image is not None:
            instance.image = image

        instance.save()
        return instance


# My Post Serializer
class MyPostSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(read_only=True)  # Use annotated field
    commented_users = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True, allow_null=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'image_url',
            'title',
            'category_name',
            'content',
            'created_at',
            'comment_count',
            'commented_users',
            'comments'
        ]

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

    def get_commented_users(self, obj):
        # Use prefetched comments
        comments = obj._prefetched_objects_cache.get('comments', [])
        users = {comment.user.id: comment.user for comment in comments}.values()
        max_users = 5
        user_list = list(users)[:max_users]
        return {
            'avatars': UserSerializer(user_list, many=True, context=self.context).data,
        }


# FAQ Serializer
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category']


class FAQCategorySerializer(serializers.ModelSerializer):
    faqs = FAQSerializer(many=True, read_only=True)

    class Meta:
        model = FAQCategory
        fields = ['id', 'name', 'faqs']


# Contact Us Serializer
class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'platform', 'icon_url', 'link']


# Notification Setting Serializer
class NotificationSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSetting
        fields = ['id', 'comments_on_posts', 'like_on_comments', 'trending_topics', 'my_recommendations', 'posts_on_my_interests']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.id
        return data


# App information Serializer
class AppInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppInfo
        fields = "__all__"
