from django.db import models
from django.conf import settings
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


class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.subcategory_name


# Topic Tags
class TopicTag(models.Model):
    tag_names = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.tag_names


# Topic
class Topic(models.Model):
    name = models.CharField(max_length=255)
    topic_tags = models.ForeignKey(TopicTag, on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


# General Facts
class GeneralFact(models.Model):
    general_definition = models.TextField()
    general_points = models.TextField()
    general_fun_fact = models.TextField()
    general_created_at = models.DateField()
    key_facts_text = models.TextField()
    key_facts_fun_fact = models.TextField()
    key_facts_created_at = models.DateField()
    picture_url = models.URLField()
    picture_created_at = models.DateField()


# News
class News(models.Model):
    news_text = models.TextField()
    news_fun_facts = models.TextField()
    news_oldest_article_date = models.DateField()
    news_newest_article_date = models.DateField()
    news_picture_url = models.URLField()
    news_picture_created_at = models.DateField()


# Interesting Trivia
class InterestingTrivia(models.Model):
    trivia_text = models.TextField()
    picture_url = models.URLField()
    trivia_fun_fact = models.TextField()
    trivia_text_created_at = models.DateField()
    trivia_picture_created_at = models.DateField()


# Opinions
class Opinion(models.Model):
    opinions_text = models.TextField()
    opinions_fun_fact = models.TextField()
    opinions_created_at = models.DateField()


# Questions
class Question(models.Model):
    questions_text = models.TextField()
    questions_fun_fact = models.TextField()
    questions_created_at = models.DateField()


# Response
class Response(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    general_fact = models.ForeignKey(GeneralFact, on_delete=models.SET_NULL, null=True)
    news = models.ForeignKey(News, on_delete=models.SET_NULL, null=True)
    interesting_trivia = models.ForeignKey(InterestingTrivia, on_delete=models.SET_NULL, null=True)
    opinion = models.ForeignKey(Opinion, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    further_key_words = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)


# Options
class Option(models.Model):
    options = models.TextField()
    selection = models.TextField()


# Search
class Search(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='searches')
    search_term = models.TextField()
    response = models.ForeignKey(Response, on_delete=models.SET_NULL, null=True)
    options = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# Search Tags
class SearchTag(models.Model):
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    tag_names = models.TextField()
    created_at = models.DateField(auto_now_add=True)


# Recommendations
class Recommendation(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
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
            models.Index(fields=['category', 'subcategory', 'topic']),
        ]


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


class UpdateMeUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    update_me = models.ForeignKey(UpdateMe, on_delete=models.CASCADE)
    clicked_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.name


# Keywords
class KeyWord(models.Model):
    key_words = models.TextField()


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


# User-Interaction Tables
class TrendingUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trending = models.ForeignKey(Trending, on_delete=models.CASCADE)
    clicked_at = models.DateField()


class RecommendationUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    clicked_at = models.DateField()


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
        return f'Bookmark'

# Preferences
class Preference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
    category = models.ManyToManyField(Category, blank=True)
    subcategory = models.ManyToManyField(Subcategory, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.name
