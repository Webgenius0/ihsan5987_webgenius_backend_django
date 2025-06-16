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
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
class Interest(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
class UserInterests(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_interests')
    interests = models.ManyToManyField(Interest, related_name='user_interests')
    selected_interests = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.email}'s interests"
    
class UserPreference(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    clicked_at = models.DateTimeField(auto_now=True)  # When user interacted with it

    class Meta:
        unique_together = ('user', 'interest')  # Avoid duplicate records

    def __str__(self):
        return f"{self.user.email} clicked {self.interest.name}"

<<<<<<< Updated upstream
=======
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
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null = True, blank = True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    headline = models.TextField()
    description = models.TextField()
    content = models.TextField()
    picture_url = models.URLField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    last_refresh = models.DateField()

# Update Me
class UpdateMe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null = True, blank = True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null = True, blank = True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    short_info = models.JSONField()
    reference_url = models.JSONField()
    background_story = models.JSONField()
    picture_url = models.TextField()
    created_at = models.DateField()
    interest = models.BooleanField()

# Keywords
class KeyWord(models.Model):
    key_words = models.TextField()

# Trending
class Trending(models.Model):
    key_words = models.ForeignKey(KeyWord, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null = True, blank = True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null = True, blank = True)
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
    from apps.community_hubs.models import Post

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trending = models.ForeignKey(Trending, on_delete=models.SET_NULL, null=True, blank=True)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.SET_NULL, null=True, blank=True)
    update_me = models.ForeignKey(UpdateMe, on_delete=models.CASCADE, null=True)
    search = models.ForeignKey(Search, on_delete=models.SET_NULL, null=True, blank=True)
    community_post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True)

# Preferences
class Preference(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null = True, blank = True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null = True, blank = True)
    created_at = models.DateField(auto_now_add=True)
>>>>>>> Stashed changes
