from django.db import models
from apps.users.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = CloudinaryField('image', null=True, blank=True)

    @property
    def image_url(self):
        if self.image:
            return self.image.url  # Cloudinary provides full URL
        return None

    def __str__(self):
        return f"{self.user.name} - {self.user.email}"