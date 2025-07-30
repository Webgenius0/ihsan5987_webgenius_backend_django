from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    Category,
    Subcategory,
    TopicTag,
    Topic,
    GeneralFact,
    News,
    InterestingTrivia,
    Opinion,
    Question,
    Response,
    Option,
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


# GeneralFact
@admin.register(GeneralFact)
class GeneralFactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "general_definition",
        "general_created_at",
        "key_facts_created_at",
        "picture_created_at",
    )
    search_fields = ("general_definition", "general_fun_fact", "key_facts_text")
    ordering = ("id",)
    list_per_page = 10


# News
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "news_oldest_article_date",
        "news_newest_article_date",
        "news_picture_url",
    )
    search_fields = ("news_text", "news_fun_facts")
    ordering = ("id",)
    list_per_page = 10


# InterestingTrivia
@admin.register(InterestingTrivia)
class InterestingTriviaAdmin(admin.ModelAdmin):
    list_display = ("id", "trivia_text_created_at", "picture_url")
    search_fields = ("trivia_text", "trivia_fun_fact")
    ordering = ("id",)
    list_per_page = 10


# Opinion
@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "opinions_created_at",
    )
    search_fields = ("opinions_text", "opinions_fun_fact")
    ordering = ("id",)
    list_per_page = 10


# Question
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "questions_created_at",
    )
    search_fields = ("questions_text", "questions_fun_fact")
    ordering = ("id",)
    list_per_page = 10


# Response
@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "subcategory",
        "topic",
        "general_fact",
        "news",
        "interesting_trivia",
        "opinion",
        "question",
        "created_at",
    )
    list_filter = ("category", "subcategory", "topic", "created_at")
    search_fields = ("further_key_words",)
    ordering = ("id",)
    list_per_page = 10


# Option
@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("id", "options", "selection")
    search_fields = ("options", "selection")
    ordering = ("id",)
    list_per_page = 10


# Search
@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "search_term", "response", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("search_term",)
    ordering = ("id",)
    list_per_page = 10


# SearchTag
@admin.register(SearchTag)
class SearchTagAdmin(admin.ModelAdmin):
    list_display = ("id", "search", "tag_names", "created_at")
    search_fields = ("tag_names",)
    ordering = ("id",)
    list_per_page = 10


# Recommendation
@admin.register(Recommendation)
class RecommendationAdmin(ModelAdmin):
    list_display = ("topic", "category","subcategory", "headline", "created_at", "last_refresh")
    # list_filter = ('category', 'created_at')
    # search_fields = ('headline', 'description', 'content')
    # ordering = ('id',)
    # list_per_page = 10


@admin.register(UpdateMe)
class UpdateMeAdmin(ModelAdmin):
    list_display = ("topic", "category", "subcategory", "created_at", "interest")
    list_filter = ("created_at", "interest", "category", "subcategory", "topic")
    search_fields = ("short_info", "background_story", "reference_url")
    ordering = ("-id",)
    list_per_page = 10


# KeyWord
@admin.register(KeyWord)
class KeyWordAdmin(admin.ModelAdmin):
    list_display = ("id", "key_words")
    search_fields = ("key_words",)
    ordering = ("id",)
    list_per_page = 10


# Trending
@admin.register(Trending)
class TrendingAdmin(ModelAdmin):
    list_display = ("id", "description", "why_trending", "picture_url", "created_at")
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
class PreferenceAdmin(ModelAdmin):
    list_display = ("user__name", "created_at")
    search_fields = ("user__username",)
