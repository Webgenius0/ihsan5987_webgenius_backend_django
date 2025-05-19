from rest_framework import serializers
from .models import Notification
from django.utils.timesince import timesince
from django.utils import timezone
import re
from apps.community_hubs.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)
    # profile_image = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    post_image = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'message', 'timestamp', 'post_image', 'is_read', 'category']
        read_only_fields = ['id', 'timestamp', 'is_read', 'category']

    def get_name(self, obj):
        print(f"Serializer get_name - sender: {obj.sender}, type: {type(obj.sender)}")
        if obj.sender:
            print(f"Sender name: {obj.sender.name}")
        else:
            print("Sender is None")
        return obj.sender.name if obj.sender else None

    def get_profile_image(self, obj):
        if obj.sender:
            print(f"Serializer get_profile_image - sender has profile? {hasattr(obj.sender, 'profile')}")
            if hasattr(obj.sender, 'profile'):
                print(f"Profile image_url: {obj.sender.profile.image_url}")
        else:
            print("Sender is None in get_profile_image")
        return obj.sender.profile.image_url if (obj.sender and hasattr(obj.sender, 'profile')) else None



    def get_post_image(self, obj):
        try:
            return obj.related_post.image.url if obj.related_post and obj.related_post.image else None
        except Exception:
            return None

    def get_timestamp(self, obj):
        created_at = obj.created_at
        now = timezone.now()
        time_diff = timesince(created_at, now).split(",")[0]
        time_str = created_at.strftime("%I:%M %p")

        if time_diff.lower() == '0 minutes':
            return f"Today | {time_str}"
        elif re.match(r'^\d+\s(day|days)', time_diff):
            days = re.match(r'(\d+)\s(day|days)', time_diff).group(1)
            return f"{days}d ago | {time_str}"
        elif re.match(r'^\d+\s(hour|hours)', time_diff):
            hours = re.match(r'(\d+)\s(hour|hours)', time_diff).group(1)
            if int(hours) < 24:
                return f"{hours}h ago | {time_str}"
        elif time_diff.lower() == '1 day':
            return f"Yesterday | {time_str}" if created_at < now else f"Tomorrow | {time_str}"
        return f"{time_diff} ago | {time_str}"

class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['is_read']