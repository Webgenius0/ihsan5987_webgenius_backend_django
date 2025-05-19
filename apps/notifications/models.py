from django.db import models
from apps.users.models import User
from cloudinary.models import CloudinaryField
from apps.community_hubs.models import Post, Comment, Like


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('post', 'New Post'),
        ('comment', 'New Comment'),
        ('like', 'Comment Like'),
    )
    CATEGORIES = (
        ('general', 'General'),
        ('system', 'System'),
    )

    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_notifications")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    category = models.CharField(max_length=20, choices=CATEGORIES, default='general')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
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