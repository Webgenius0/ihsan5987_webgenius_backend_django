from rest_framework import serializers
from .models import Notification
from .gnews_service import human_readable_time  # import the time formatter
from datetime import datetime, timedelta

class NotificationSerializer(serializers.ModelSerializer):
    actor_name = serializers.SerializerMethodField()
    actor_image = serializers.SerializerMethodField()
    time_display = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'notif_type', 'category', 'actor_name', 'actor_image',
            'post_title', 'post_image', 'message', 'icon_url',
            'is_read', 'is_new', 'time_display'
        ]

    def get_actor_name(self, obj):
        return obj.actor_user.get_full_name() if obj.actor_user else None

    def get_actor_image(self, obj):
        return obj.actor_user.profile.image.url if obj.actor_user and hasattr(obj.actor_user, 'profile') else None

    def get_time_display(self, obj):
        return human_readable_time(obj.created_at)

    def get_is_new(self, obj):
        return not obj.is_read and obj.created_at.date() == datetime.today().date()
