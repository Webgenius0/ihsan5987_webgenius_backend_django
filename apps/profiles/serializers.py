from rest_framework import serializers
from apps.community_hubs.models import Post
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', required=False)

    class Meta:
        model = Profile
        fields = ['image_url', 'name']  # name is now part of the serializer

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
    
class MyPostSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(source='user.profile', read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'content', 'created_at', 'comment_count', 'user']

    def get_comment_count(self, obj):
        return obj.comment_count()