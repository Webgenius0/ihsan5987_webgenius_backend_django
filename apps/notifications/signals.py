from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.community_hubs.models import Post, Comment, Like
from apps.users.models import User
from .services import send_notification

@receiver(post_save, sender=Post)
def notify_on_post_creation(sender, instance, created, **kwargs):
    if created:
        users = User.objects.exclude(id=instance.user.id)
        print("users", users)
        message = f"{instance.user.name} created a new post: {instance.title}"
        print("message", message)

        for user in users:
            send_notification(
                sender=instance.user,  # ✅ Use instance.user here
                recipient=user,
                notification_type='post',
                message=message,
                related_post=instance
            )
            print("send notification from signal", send_notification)


@receiver(post_save, sender=Comment)
def notify_on_comment_creation(sender, instance, created, **kwargs):
    if created:
        post_creator = instance.post.user
        if post_creator != instance.user:
            message = f"{instance.user.name} commented on your post: {instance.post.title}"
            send_notification(
                sender=instance.user,  # ✅ Use instance.user here
                recipient=post_creator,
                notification_type='comment',
                message=message,
                related_post=instance.post,
                related_comment=instance
            )

@receiver(post_save, sender=Like)
def notify_on_like_creation(sender, instance, created, **kwargs):
    if created:
        comment_creator = instance.comment.user
        if comment_creator != instance.user:
            message = f"{instance.user.name} liked your comment on: {instance.comment.post.title}"
            send_notification(
                sender=instance.user,  # ✅ Use instance.user here
                recipient=comment_creator,
                notification_type='like',
                message=message,
                related_post=instance.comment.post,
                related_comment=instance.comment
            )