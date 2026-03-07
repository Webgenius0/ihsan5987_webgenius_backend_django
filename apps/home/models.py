from django.db import models
from django.conf import settings
from auditlog.registry import auditlog
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

User = get_user_model()


# Category & Subcategory
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)
    
    def __str__(self):
        return self.category_name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    subcategory_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.subcategory_name}'


# Search
class Search(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='search')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True, related_name='search')
    topic = models.CharField(max_length=200, blank=True, null=True)
    general_fact = models.JSONField(blank=True, null=True)
    news = models.JSONField(blank=True, null=True)
    interesting_trivia = models.JSONField(blank=True, null=True)
    opinion = models.JSONField(blank=True, null=True)
    question = models.JSONField(blank=True, null=True)
    further_key_words = models.JSONField(blank=True, null=True)
    search_term = models.CharField(
        max_length=200, blank=True, null=True
    )  # for getting same result for 2nd time search. after some time it will remove by scheduler
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Search - {self.topic}"
    
    class Meta:
        indexes = [
            models.Index(fields=['category', 'subcategory']),
        ]


class SearchHistory(models.Model):
    """SEARCH HISTORY FOR EACH USERS"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='search_history')
    search_term = models.CharField(max_length=200)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Search History for {self.user} - {self.search_term}'


# Recommendations
class Recommendation(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.CharField(max_length=255, blank=True, null=True)
    headline = models.TextField(blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    key_tips_and_takeaways = models.JSONField(blank=True, null=True)
    fun_facts = models.JSONField(blank=True, null=True)
    conclusion = models.TextField(blank=True, null=True)
    picture_url = models.URLField(blank=True, null=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    last_refresh = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.topic or f"Recommendation #{self.pk or 'new'}"

    class Meta:
        verbose_name_plural = "Recommendations"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'subcategory']),
        ]


# Update Me
class UpdateMe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.CharField(max_length=255, blank=True, null=True)
    short_info = models.JSONField(blank=True, null=True)
    reference_url = models.JSONField(blank=True, null=True)
    background_story = models.JSONField(blank=True, null=True)
    picture_url = models.URLField(blank=True, null=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    is_archive = models.BooleanField(default=False)
    is_top3 = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # interest = models.BooleanField(default=False)

    def __str__(self):
        return self.topic or f"UpdateMe #{self.pk or 'new'}"

    class Meta:
        verbose_name_plural = "Update Me"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'subcategory']),
        ]


# Trending
class Trending(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    why_trending = models.JSONField(blank=True, null=True)
    key_points = models.JSONField(blank=True, null=True)
    outlook = models.JSONField(blank=True, null=True)
    picture_url = models.URLField(blank=True, null=True, max_length=500)
    links_and_sources = models.JSONField(blank=True, null=True)
    picture_last_refresh = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        snippet = (self.description or self.topic or "").strip()
        if snippet:
            return f"Trending - {snippet[:20]}"
        return f"Trending #{self.pk or 'new'}"

    class Meta:
        indexes = [
            models.Index(fields=['category', 'subcategory']),
        ]


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    obj = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_label = getattr(self.user, "name", None) or getattr(self.user, "username", None) or str(self.user_id)
        return f"Bookmark - {user_label}"


# Preferences
class Preference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
    category = models.ManyToManyField(Category, blank=True)
    subcategory = models.ManyToManyField(Subcategory, blank=True)
    
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return getattr(self.user, "name", None) or getattr(self.user, "username", None) or f"User #{self.user_id}"


# Register model for audit logging
auditlog.register(Preference)
