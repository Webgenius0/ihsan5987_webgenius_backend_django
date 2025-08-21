import re
from .models import Notification
from django.utils import timezone
from rest_framework import serializers
from django.utils.timesince import timesince
from apps.community_hubs.serializers import UserSerializer


class GeneralNotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)
    profile_image = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    post_image = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'profile_image', 'message', 'timestamp', 'post_image', 'category', 'is_read']
        read_only_fields = ['id', 'timestamp', 'category', 'is_read']

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


class SystemNotificationSerializer(serializers.ModelSerializer):
    new = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'title', 'icon', 'message', 'timestamp', 'is_read', 'category', 'new']
        read_only_fields = ['id', 'timestamp', 'is_read', 'category', 'icon', 'new']

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

    def get_new(self, obj):
        return not obj.is_read

    def get_icon(self, obj):
        icon_key = obj.system_event
        print(f"Serializer get_icon - icon_key: {icon_key}")
        return Notification.CLOUDINARY_ICON_MAP.get(icon_key)


class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['is_read']

