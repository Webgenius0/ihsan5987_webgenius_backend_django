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


@admin.register(Subcategory)
class SubcategoryAdmin(ModelAdmin):
    list_display = ("subcategory_name", "created_at")
    search_fields = ("subcategory_name",)


# TopicTag & Topic
@admin.register(TopicTag)
class TopicTagAdmin(admin.ModelAdmin):
    list_display = ("id", "tag_names", "created_at")
    search_fields = ("tag_names",)


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
    # list_filter = ('category', 'created_at')
    # search_fields = ('headline', 'description', 'content')
    # ordering = ('id',)
    # list_per_page = 10


@admin.register(UpdateMe)
class UpdateMeAdmin(admin.ModelAdmin):
    list_display = ("topic", "category", "subcategory", "created_at", "interest")
    list_filter = ("created_at", "interest", "category", "subcategory", "topic")
    search_fields = ("short_info", "background_story", "reference_url")
    ordering = ("-id",)
    list_per_page = 10

    # optimize queryset
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("category", "subcategory", "topic")
        return qs
# KeyWord
@admin.register(KeyWord)
class KeyWordAdmin(admin.ModelAdmin):
    list_display = ("id", "key_words")
    search_fields = ("key_words",)
    ordering = ("id",)
    list_per_page = 10


# Trending
@admin.register(Trending)
class TrendingAdmin(admin.ModelAdmin):
    list_display = ("id", "picture_url", "created_at")
    list_filter = ("created_at",)
    search_fields = ("description", "why_trending", "key_points", "outlook")
    ordering = ("id",)
    list_per_page = 10


# TrendingUser
@admin.register(TrendingUser)
class TrendingUserAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "trending", "clicked_at")
    list_filter = ("clicked_at", "user")
    search_fields = ("user__username",)
    ordering = ("id",)
    list_per_page = 10


# RecommendationUser
@admin.register(RecommendationUser)
class RecommendationUserAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recommendation", "clicked_at")
    list_filter = ("clicked_at", "user")
    search_fields = ("user__username",)
    ordering = ("id",)
    list_per_page = 10


# Bookmark
@admin.register(Bookmark)
class BookmarkAdmin(ModelAdmin):
    pass


# Preference
@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ("user__name", "created_at")
    search_fields = ("user__username",)
