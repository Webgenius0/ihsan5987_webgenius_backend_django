from django.db import models
from django.conf import settings
from apps.community_hubs.models import Post

# Category & Subcategory
class Category(models.Model):
    category_name = models.CharField(max_length=200, default="Unknown-Category")
    created_at = models.DateField(auto_now_add=True)

class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length=200, default="Unknown-SubCategory")
    created_at = models.DateField(auto_now_add=True)

# Topic Tags
class TopicTag(models.Model):
    tag_names = models.TextField()
    created_at = models.DateField(auto_now_add=True)

# Topic
class Topic(models.Model):
    name = models.CharField(max_length=255)
    topic_tags = models.ForeignKey(TopicTag, on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(auto_now_add=True)

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    headline = models.TextField()
    description = models.TextField()
    content = models.TextField()
    picture_url = models.URLField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    last_refresh = models.DateField()

# Keywords
class KeyWord(models.Model):
    key_words = models.TextField()

# Trending
class Trending(models.Model):
    key_words = models.ForeignKey(KeyWord, on_delete=models.CASCADE)
    description = models.TextField()
    why_trending = models.TextField()
    key_points = models.TextField()
    outlook = models.TextField()
    picture_url = models.URLField(blank=True, null=True)
    picture_last_refresh = models.DateField()
    created_at = models.DateField(auto_now_add=True)

# User-Interaction Tables
class TrendingUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trending = models.ForeignKey(Trending, on_delete=models.CASCADE)
    clicked_at = models.DateField()

class RecommendationUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)
    clicked_at = models.DateField()

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trending = models.ForeignKey(Trending, on_delete=models.SET_NULL, null=True, blank=True)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.SET_NULL, null=True, blank=True)
    search = models.ForeignKey(Search, on_delete=models.SET_NULL, null=True, blank=True)
    community_post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True)

# Preferences
class Preference(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

# # Bookmark model
# class NewsBookmark(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
#     article = models.ForeignKey(TrendingNews, on_delete=models.CASCADE, related_name='bookmarks')
#     bookmarked_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'article')


# #Interest model
# class Category(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

# class SubCategory(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return f"{self.category.name} - {self.name}"
    
# class Interest(models.Model):
#     name = models.CharField(max_length=255)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
#     subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return self.name
    
# class UserInterests(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_interests')
#     interests = models.ManyToManyField(Interest, related_name='user_interests')
#     selected_interests = models.IntegerField(default=0)

#     def __str__(self):
#         return f"{self.user.email}'s interests"
    
# class UserPreference(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
#     interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
#     clicked_at = models.DateTimeField(auto_now=True)  # When user interacted with it

#     class Meta:
#         unique_together = ('user', 'interest')  # Avoid duplicate records

#     def __str__(self):
#         return f"{self.user.email} clicked {self.interest.name}"

