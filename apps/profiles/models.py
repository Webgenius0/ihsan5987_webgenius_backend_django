from django.db import models
from apps.users.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', default='default.jpg', null=True)

    def __str__(self):
        return f"{self.user.name} - {self.user.email}"