from django.db import models
from django.conf import settings

#Trending News model
class TrendingNews(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)
    image = models.URLField(null=True, blank=True)
    published_at = models.DateTimeField()
    source_name = models.CharField(max_length=255, null=True, blank=True)
    source_url = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
class RecommendedNews(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)
    image = models.URLField(null=True, blank=True)
    published_at = models.DateTimeField()
    source_name = models.CharField(max_length=255, null=True, blank=True)
    source_url = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title

# Bookmark model
class NewsBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    article = models.ForeignKey(TrendingNews, on_delete=models.CASCADE, related_name='bookmarks')
    bookmarked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')


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
