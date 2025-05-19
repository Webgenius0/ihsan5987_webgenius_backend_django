from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ('id', 'sender', 'recipient', 'category', 'notification_type', 'message', 'related_post', 'related_comment', 'image', 'is_read', 'created_at')