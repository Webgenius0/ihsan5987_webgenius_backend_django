from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    Category,
    Subcategory,
    TopicTag,
    Topic,
    SearchOption,
    SearchHistory,
    Search,
    SearchTag,
    Recommendation,
    KeyWord,
    Trending,
    TrendingUser,
    RecommendationUser,
    Bookmark,
    Preference,
    UpdateMe,
)


# Category & Subcategory
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("category_name", "created_at")
    search_fields = ("category_name",)
    ordering = ("-created_at",)
    list_per_page = 20


@admin.register(Subcategory)
class SubcategoryAdmin(ModelAdmin):
    list_display = ("subcategory_name", "created_at")
    search_fields = ("subcategory_name",)
    ordering = ("-created_at",)
    list_per_page = 20


# TopicTag & Topic
@admin.register(TopicTag)
class TopicTagAdmin(ModelAdmin):
    list_display = ("tag_names", "created_at")
    search_fields = ("tag_names",)
    ordering = ("-created_at",)
    list_per_page = 20


@admin.register(Topic)
class TopicAdmin(ModelAdmin):
    list_display = ("name", "topic_tags", "created_at")
    search_fields = ("name", "topic_tags")
    list_filter = ("topic_tags",)


# Option
@admin.register(SearchOption)
class SearchOptionAdmin(admin.ModelAdmin):
    pass


# Search
@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    pass


# SearchTag
@admin.register(SearchTag)
class SearchTagAdmin(admin.ModelAdmin):
    pass


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    pass


# Recommendation
@admin.register(Recommendation)
class RecommendationAdmin(ModelAdmin):
    list_display = ("topic", "category","subcategory", "headline", "created_at", "last_refresh")
    list_filter = ('category', 'created_at')
    search_fields = ('headline', 'description', 'content')
    ordering = ('-created_at',)
    list_per_page = 20


@admin.register(UpdateMe)
class UpdateMeAdmin(ModelAdmin):
    list_display = ("topic", "category", "subcategory", "created_at", "interest")
    list_filter = ("created_at", "interest", "category", "subcategory", "topic")
    search_fields = ("short_info", "background_story", "reference_url")
    ordering = ("-created_at",)
    list_per_page = 20


# KeyWord
@admin.register(KeyWord)
class KeyWordAdmin(ModelAdmin):
    list_display = ("id", "key_words")
    search_fields = ("key_words",)
    list_per_page = 20


# Trending
@admin.register(Trending)
class TrendingAdmin(ModelAdmin):
    list_display = ("description", "why_trending", "picture_url", "created_at")
    list_filter = ("created_at",)
    search_fields = ("description", "why_trending", "key_points", "outlook")
    list_per_page = 20


# TrendingUser
@admin.register(TrendingUser)
class TrendingUserAdmin(ModelAdmin):
    list_display = ("user", "trending", "clicked_at")
    list_filter = ("clicked_at", "user")
    search_fields = ("user__username",)
    list_per_page = 20


# RecommendationUser
@admin.register(RecommendationUser)
class RecommendationUserAdmin(ModelAdmin):
    list_display = ("user", "recommendation", "clicked_at")
    list_filter = ("clicked_at", "user")
    search_fields = ("user__username",)
    list_per_page = 20


# Bookmark
@admin.register(Bookmark)
class BookmarkAdmin(ModelAdmin):
    pass


# Preference
@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ("user__name", "created_at")
    search_fields = ("user__username",)
    ordering = ("-created_at",)
    list_per_page = 20
