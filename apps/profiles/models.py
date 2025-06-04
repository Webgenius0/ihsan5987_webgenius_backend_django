from django.db import models
from apps.users.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = CloudinaryField('image', null=True, blank=True)
    premium_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def image_url(self):
        if self.image:
            return self.image.url  # Cloudinary provides full URL
        return None

    def __str__(self):
        return f"{self.user.name} - {self.user.email}"
    

class FAQCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs')

    def __str__(self):
        return self.question
    

# Contact Us
class ContactUs(models.Model):
    PLATFORM_CHOICES = [
        ('email', 'Contact Us'),
        ('whatsapp', 'WhatsApp'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('website', 'Website'),
    ]
    platform = models.CharField(max_length=50, choices= PLATFORM_CHOICES, unique=True)
    icon = CloudinaryField('icon', null=True, blank=True)
    link = models.URLField(unique=True, null=True, blank=True)

    @property
    def icon_url(self):
        if self.icon:
            return self.icon.url
        return None

class NotificationSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_setting')
    comments_on_posts = models.BooleanField(default=True)
    like_on_comments = models.BooleanField(default=True)
    trending_topics = models.BooleanField(default=True)
    my_recommendations = models.BooleanField(default=True)
    posts_on_my_interests = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name}'s notification setting"
