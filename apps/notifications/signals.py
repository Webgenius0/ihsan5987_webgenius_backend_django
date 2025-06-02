from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.community_hubs.models import Post, Comment, Like
from apps.users.models import User
from .services import send_notification
from apps.profiles.models import NotificationSetting

@receiver(post_save, sender=Post)
def notify_on_post_creation(sender, instance, created, **kwargs):
    if created:
        users = User.objects.exclude(id=instance.user.id)
        message = f"{instance.user.name} created a new post: {instance.title}"

        for user in users:
            try:
                settings = NotificationSetting.objects.get(user=user)
                if settings.posts_on_my_interests or settings.trending_topics or settings.my_recommendations:
                    send_notification(
                        sender=instance.user,  # ✅ Use instance.user here
                        recipient=user,
                        notification_type='post',
                        message=message,
                        related_post=instance
                    )
            except NotificationSetting.DoesNotExist:
                pass


@receiver(post_save, sender=Comment)
def notify_on_comment_creation(sender, instance, created, **kwargs):
    if created:
        post_creator = instance.post.user
        if post_creator != instance.user:
            try:
                settings = NotificationSetting.objects.get(user=post_creator)
                if settings.comment_on_posts:
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
