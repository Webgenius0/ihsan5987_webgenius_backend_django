from django.db import models
from apps.users.models import User
from cloudinary.models import CloudinaryField
from apps.home.models import Category


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="posts"
    )
    category = models.ForeignKey(
        'home.Category', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    content = models.TextField()
    image = CloudinaryField('image', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None

    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name="comments"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name} - {self.post.title}"


class CommentReport(models.Model):
    REASON_CHOICES = [
        ('spam', 'Spam'),
        ('abuse', 'Abuse'),
        ('offensive', 'Offensive Content'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('dismissed', 'Dismissed'),
    ]

    reporter = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reports'
    )
    comment = models.ForeignKey(
        Comment, 
        on_delete=models.CASCADE, 
        related_name='reports'
    )
    reason = models.CharField(max_length=255, choices=REASON_CHOICES)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reporter', 'comment')

    def __str__(self):
        return f"Report by {self.reporter.name} on comment {self.comment.id} - {self.status}"


class Like(models.Model):
    comment = models.ForeignKey(
        Comment, 
        related_name='likes', 
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')
