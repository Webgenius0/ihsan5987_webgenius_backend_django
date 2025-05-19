from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User

# class Notification(models.Model):
#     NOTIF_TYPE_CHOICES = (
#         ('general', 'General'),
#         ('system', 'System'),
#     )

#     CATEGORY_CHOICES = (
#         ('info', 'Info'),
#         ('success', 'Success'),
#         ('warning', 'Warning'),
#         ('security', 'Security'),
#         ('storage', 'Storage'),
#     )

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
#     notif_type = models.CharField(max_length=10, choices=NOTIF_TYPE_CHOICES)
#     receiver = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='actor_notifications')
#     post_title = models.CharField(max_length=255, blank=True, null=True)
#     post_image = models.URLField(blank=True, null=True)
#     message = models.TextField(blank=True, null=True)
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
#     icon_url = models.URLField(blank=True, null=True)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-created_at']

#Interest model
class Interest(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class UserInterests(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_interests')
    interests = models.ManyToManyField(Interest, related_name='user_interests')
    selected_interests = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s interests"
