from django.contrib import admin
from .models import (
    Category, Subcategory, TopicTag, Topic, GeneralFact, News, InterestingTrivia,
    Opinion, Question, Response, Option, Search, SearchTag, Recommendation,
    KeyWord, Trending, TrendingUser, RecommendationUser, Bookmark, Preference
)

# Category & Subcategory
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'created_at')
    search_fields = ('category_name',)
    ordering = ('-created_at',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'subcategory_name', 'created_at')
    search_fields = ('subcategory_name',)
    ordering = ('-created_at',)


# TopicTag & Topic
@admin.register(TopicTag)
class TopicTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag_names', 'created_at')
    search_fields = ('tag_names',)
    ordering = ('-created_at',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'topic_tags', 'created_at')
    search_fields = ('name',)
    list_filter = ('topic_tags',)
    ordering = ('-created_at',)


# GeneralFact
@admin.register(GeneralFact)
class GeneralFactAdmin(admin.ModelAdmin):
    list_display = ('id', 'general_created_at', 'picture_url')
    search_fields = ('general_definition', 'general_fun_fact', 'key_facts_text')
    ordering = ('-general_created_at',)


# News
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'news_oldest_article_date', 'news_newest_article_date', 'news_picture_url')
    search_fields = ('news_text', 'news_fun_facts')
    ordering = ('-news_newest_article_date',)


# InterestingTrivia
@admin.register(InterestingTrivia)
class InterestingTriviaAdmin(admin.ModelAdmin):
    list_display = ('id', 'trivia_text_created_at', 'picture_url')
    search_fields = ('trivia_text', 'trivia_fun_fact')
    ordering = ('-trivia_text_created_at',)


# Opinion
@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ('id', 'opinions_created_at',)
    search_fields = ('opinions_text', 'opinions_fun_fact')
    ordering = ('-opinions_created_at',)


# Question
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'questions_created_at',)
    search_fields = ('questions_text', 'questions_fun_fact')
    ordering = ('-questions_created_at',)


# Response
@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'category', 'subcategory', 'topic', 'general_fact', 'news', 
        'interesting_trivia', 'opinion', 'question', 'created_at'
    )
    list_filter = ('category', 'subcategory', 'topic', 'created_at')
    search_fields = ('further_key_words',)
    ordering = ('-created_at',)


# Option
@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'options', 'selection')
    search_fields = ('options', 'selection')


# Search
@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'search_term', 'response', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('search_term',)
    ordering = ('-created_at',)


# SearchTag
@admin.register(SearchTag)
class SearchTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'search', 'tag_names', 'created_at')
    search_fields = ('tag_names',)
    ordering = ('-created_at',)


# Recommendation
@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'topic', 'headline', 'created_at', 'last_refresh')
    list_filter = ('category', 'topic', 'created_at')
    search_fields = ('headline', 'description', 'content')
    ordering = ('-created_at',)


# KeyWord
@admin.register(KeyWord)
class KeyWordAdmin(admin.ModelAdmin):
    list_display = ('id', 'key_words')
    search_fields = ('key_words',)


# Trending
@admin.register(Trending)
class TrendingAdmin(admin.ModelAdmin):
    list_display = ('id', 'key_words', 'description', 'why_trending', 'picture_url', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('description', 'why_trending', 'key_points', 'outlook')
    ordering = ('-created_at',)


# TrendingUser
@admin.register(TrendingUser)
class TrendingUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'trending', 'clicked_at')
    list_filter = ('clicked_at', 'user')
    search_fields = ('user__username',)


# RecommendationUser
@admin.register(RecommendationUser)
class RecommendationUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recommendation', 'clicked_at')
    list_filter = ('clicked_at', 'user')
    search_fields = ('user__username',)


# Bookmark
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'trending', 'recommendation', 'search', 'community_post')
    list_filter = ('user',)
    search_fields = ('user__username',)


# Preference
@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'subcategory', 'created_at')
    list_filter = ('created_at', 'category', 'subcategory')
    search_fields = ('user__username',)
