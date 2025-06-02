from .models import Profile
from apps.users.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create a user profile when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


