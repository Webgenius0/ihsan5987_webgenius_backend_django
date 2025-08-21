from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.community_hubs.models import Post, Comment, Like
from apps.users.models import User
from firebase_admin import messaging
from django.db.models import Q
from .services import send_notification
from apps.notifications.models import Notification
from fcm_django.models import FCMDevice
from apps.profiles.models import NotificationSetting


@receiver(post_save, sender=Post)
def notify_on_post_creation(sender, instance, created, **kwargs):
    if not created:
        return

    # Create only one notification record (like comments/likes)
    notification = Notification.objects.create(
        sender=instance.user,
        recipient=None,   # 🚨 Make this nullable if not already
        notification_type='post',
        message=f"{instance.user.name} created a new post: {instance.title}",
        related_post=instance
    )

    # Fetch recipients based on NotificationSetting
    recipient_ids = list(
        NotificationSetting.objects.exclude(user=instance.user)
        .filter(posts_on_my_interests=True)  # apply filters as needed
        .values_list('user_id', flat=True)
    )

    # Fetch all devices at once
    devices = FCMDevice.objects.filter(user_id__in=recipient_ids, active=True)

    if devices.exists():
        devices.send_message(
            title="New Post",
            body=f"{instance.user.name} created a new post: {instance.title}",
            data={
                "notification_id": str(notification.id),
                "related_post_id": instance.id,
                "type": "post",
            }
        )


@receiver(post_save, sender=Comment)
def notify_on_comment_creation(sender, instance, created, **kwargs):
    if created:
        post_creator = instance.post.user
        if post_creator != instance.user:
            try:
                settings = NotificationSetting.objects.get(user=post_creator)
                if settings.comments_on_posts:
                    message = f"{instance.user.name} commented on your post: {instance.post.title}"
                    send_notification(
                        sender=instance.user,  # ✅ Use instance.user here
                        recipient=post_creator,
                        notification_type='comment',
                        message=message,
                        related_post=instance.post,
                        related_comment=instance
                    )
            except NotificationSetting.DoesNotExist:
                pass


@receiver(post_save, sender=Like)
def notify_on_like_creation(sender, instance, created, **kwargs):
    if created:
        comment_creator = instance.comment.user
        if comment_creator != instance.user:
            try:
                settings = NotificationSetting.objects.get(user=comment_creator)
                if settings.like_on_comments:
                    message = f"{instance.user.name} liked your comment on: {instance.comment.post.title}"
                    send_notification(
                        sender=instance.user,  # ✅ Use instance.user here
                        recipient=comment_creator,
                        notification_type='like',
                        message=message,
                        related_post=instance.comment.post,
                        related_comment=instance.comment
                    )
            except NotificationSetting.DoesNotExist:
                pass
