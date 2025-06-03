from apps.users.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile, NotificationSetting

# Create a user profile when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_notification_setting(sender, instance, created, **kwargs):
    if created:
        NotificationSetting.objects.create(user=instance)


