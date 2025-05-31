from rest_framework import serializers
from apps.community_hubs.models import Post
from apps.community_hubs.serializers import UserSerializer
from .models import Profile, FAQ, FAQCategory, ContactUs, NotificationSetting

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
    # user = ProfileSerializer(source='user.profile', read_only=True)
    comment_count = serializers.SerializerMethodField()
    commented_users = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['id', 'image', 'title', 'category', 'content', 'created_at', 'comment_count', 'commented_users']

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
        }

    def get_comment_count(self, obj):
        return obj.comment_count()
    
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
        fields = ['id', 'comment_on_posts', 'like_on_comments', 'trending_topics', 'my_recommendations', 'posts_on_my_interests']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.id
        return data
