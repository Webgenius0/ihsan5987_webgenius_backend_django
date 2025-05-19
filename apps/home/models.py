from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User

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
