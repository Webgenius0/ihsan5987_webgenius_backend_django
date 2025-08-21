from django.db import models
from apps.users.models import User
from auditlog.registry import auditlog
from cloudinary.models import CloudinaryField
from apps.community_hubs.models import Post, Comment


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('post', 'New Post'),
        ('comment', 'New Comment'),
        ('like', 'Comment Like'),
        ('system', 'System Alert'),
    )
    CATEGORIES = (
        ('general', 'General'),
        ('system', 'System'),
    )

    SYSTEM_EVENTS = (
        ('account_complete', 'Account Completed'),
        ('wrong_password', 'Wrong Password Attempt'),
        ('new_device_login', 'New Device Login'),
        ('password_change', 'Password Change'),
        # Add more as needed
    )

    CLOUDINARY_ICON_MAP = {
        'account_complete': 'https://res.cloudinary.com/dmm41aaoh/image/upload/v1748597960/complete.png',
        'wrong_password': 'https://res.cloudinary.com/dmm41aaoh/image/upload/v1748597960/warning.png',
        'new_device_login': 'https://res.cloudinary.com/dmm41aaoh/image/upload/v1748597960/security.png',
        'password_change': 'https://res.cloudinary.com/dmm41aaoh/image/upload/v1748597959/updates.png',
        # 'default': 'https://res.cloudinary.com/dmm41aaoh/image/upload/v1748597959/updates.png',
    }

    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_notifications")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    category = models.CharField(max_length=20, choices=CATEGORIES, default='general')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    system_event = models.CharField(max_length=30, choices=SYSTEM_EVENTS, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    icon = models.CharField(max_length=100, null=True, blank=True)
    related_post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    related_comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)
    image = CloudinaryField('image', null=True, blank=True)  # Add image field
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient.name} - {self.category} - {self.notification_type} - {self.message}"

    class Meta:
        ordering = ['-created_at']

    @property
    def formatted_time(self):
        from django.utils import timezone
        time_diff = timezone.now() - self.created_at
        if time_diff.days == 0:
            return f"Today | {self.created_at.strftime('%I:%M %p')}"
        elif time_diff.days == 1:
            return f"Yesterday | {self.created_at.strftime('%I:%M %p')}"
        elif time_diff.days < 7:
            return f"{time_diff.days} day(s) ago | {self.created_at.strftime('%I:%M %p')}"
        return self.created_at.strftime('%Y-%m-%d | %I:%M %p')

    def save(self, *args, **kwargs):
        if self.system_event in self.CLOUDINARY_ICON_MAP:
            self.icon = self.CLOUDINARY_ICON_MAP[self.system_event]
        super().save(*args, **kwargs)


# Register model for audit logging
# auditlog.register(Notification)
