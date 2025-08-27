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
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.category_name


# Register model for audit logging
auditlog.register(Category)


class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.subcategory_name


# Register model for audit logging
auditlog.register(Subcategory)


# # Topic Tags
# class TopicTag(models.Model):
#     tag_names = models.TextField()
#     created_at = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.tag_names


# # Register model for audit logging
# auditlog.register(TopicTag)


# Topic
class Topic(models.Model):
    name = models.CharField(max_length=255)
    # topic_tags = models.ForeignKey(TopicTag, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


# Search
class Search(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='search')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True, related_name='search')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True, related_name='search')
    general_fact = models.JSONField(blank=True, null=True)
    news = models.JSONField(blank=True, null=True)
    interesting_trivia = models.JSONField(blank=True, null=True)
    opinion = models.JSONField(blank=True, null=True)
    question = models.JSONField(blank=True, null=True)
    further_key_words = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    search_term = models.CharField(
        max_length=200, blank=True, null=True
    )  # for getting same result for 2nd time search. after some time it will remove by scheduler

    def __str__(self):
        return f"Search - {self.topic.name}"


# Register model for audit logging
auditlog.register(Search)


# Search Tags
class SearchTag(models.Model):
    """SEARCH TERM, USED FOR SEARCHING"""
    # search = models.ForeignKey(Search, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.tag_name

    def save(self, *args, **kwargs):
        self.tag_name = self.tag_name.lower()
        super(SearchTag, self).save(*args, **kwargs)


# Register model for audit logging
auditlog.register(SearchTag)


class SearchOption(models.Model):
    """GENERATED OPTIONS FOR SEARCHING"""
    search_tag = models.ForeignKey(SearchTag, on_delete=models.CASCADE, related_name='options')
    keyword = models.CharField(max_length=200)
    category = models.CharField(max_length=200, blank=True, null=True)
    subcategory = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Option for {self.search_tag.tag_name} - {self.keyword}'


# Register model for audit logging
auditlog.register(SearchOption)


class SearchHistory(models.Model):
    """SEARCH HISTORY FOR EACH USERS"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='search_history')
    search_term = models.CharField(max_length=200)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Search History for {self.user} - {self.search_term}'


# Register model for audit logging
auditlog.register(SearchHistory)


# Recommendations
class Recommendation(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    headline = models.TextField(blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    key_tips_and_takeaways = models.JSONField(blank=True, null=True)
    fun_facts = models.JSONField(blank=True, null=True)
    conclusion = models.TextField(blank=True, null=True)
    # description = models.TextField()
    # content = models.TextField()
    picture_url = models.URLField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    last_refresh = models.DateField(auto_now=True)

    def __str__(self):
        return self.topic.name

    class Meta:
        verbose_name_plural = "Recommendations"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'topic']),
        ]


# Register model for audit logging
auditlog.register(Recommendation)


# Update Me
class UpdateMe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    short_info = models.JSONField(blank=True, null=True)
    reference_url = models.JSONField(blank=True, null=True)
    background_story = models.JSONField(blank=True, null=True)
    picture_url = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    interest = models.BooleanField(default=False)

    def __str__(self):
        return self.topic.name

    class Meta:
        verbose_name_plural = "Update Me"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'subcategory', 'topic']),
        ]


# Register model for audit logging
auditlog.register(UpdateMe)


# class UpdateMeUser(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     update_me = models.ForeignKey(UpdateMe, on_delete=models.CASCADE)
#     clicked_at = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.user.name


# Register model for audit logging
# auditlog.register(UpdateMeUser)


# Keywords
# class KeyWord(models.Model):
#     key_words = models.TextField()


# Trending
class Trending(models.Model):
    # key_words = models.ForeignKey(KeyWord, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    why_trending = models.JSONField(blank=True, null=True)
    key_points = models.JSONField(blank=True, null=True)
    outlook = models.JSONField(blank=True, null=True)
    picture_url = models.URLField(blank=True, null=True)
    picture_last_refresh = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Trending - {self.description[:20]}"


# Register model for audit logging
auditlog.register(Trending)


# User-Interaction Tables
# class TrendingUser(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     trending = models.ForeignKey(Trending, on_delete=models.CASCADE)
#     clicked_at = models.DateField()


# # Register model for audit logging
# auditlog.register(TrendingUser)


# class RecommendationUser(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
#     clicked_at = models.DateField()


# # Register model for audit logging
# auditlog.register(RecommendationUser)


# class Bookmark(models.Model):
#     from apps.community_hubs.models import Post

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     trending = models.ForeignKey(Trending, on_delete=models.SET_NULL, null=True, blank=True)
#     recommendation = models.ForeignKey(Recommendation, on_delete=models.SET_NULL, null=True, blank=True)
#     update_me = models.ForeignKey(UpdateMe, on_delete=models.CASCADE, null=True)
#     search = models.ForeignKey(Search, on_delete=models.SET_NULL, null=True, blank=True)
#     community_post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True)


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    obj = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bookmark - {self.user.name}"


# Register model for audit logging
auditlog.register(Bookmark)


# Preferences
class Preference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
    category = models.ManyToManyField(Category, blank=True)
    subcategory = models.ManyToManyField(Subcategory, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.name


# Register model for audit logging
auditlog.register(Preference)
