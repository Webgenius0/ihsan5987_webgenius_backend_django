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
    ordering = ("-created_at",)
    list_per_page = 20


# GeneralFact
@admin.register(GeneralFact)
class GeneralFactAdmin(ModelAdmin):
    list_display = (
        "general_definition",
        "general_created_at",
        "key_facts_created_at",
        "picture_created_at",
    )
    search_fields = ("general_definition", "general_fun_fact", "key_facts_text")
    list_per_page = 20


# News
@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = (
        "news_oldest_article_date",
        "news_newest_article_date",
        "news_picture_url",
    )
    search_fields = ("news_text", "news_fun_facts")
    list_per_page = 20


# InterestingTrivia
@admin.register(InterestingTrivia)
class InterestingTriviaAdmin(ModelAdmin):
    list_display = ("trivia_text_created_at", "picture_url")
    search_fields = ("trivia_text", "trivia_fun_fact")
    list_per_page = 20


# Opinion
@admin.register(Opinion)
class OpinionAdmin(ModelAdmin):
    list_display = (
        "id",
        "opinions_created_at",
    )
    search_fields = ("opinions_text", "opinions_fun_fact")
    list_per_page = 20


# Question
@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = (
        "id",
        "questions_created_at",
    )
    search_fields = ("questions_text", "questions_fun_fact")
    list_per_page = 20


# Response
@admin.register(Response)
class ResponseAdmin(ModelAdmin):
    list_display = (
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
    ordering = ("-created_at",)
    list_per_page = 20


# Option
@admin.register(Option)
class OptionAdmin(ModelAdmin):
    list_display = ("options", "selection")
    search_fields = ("options", "selection")
    list_per_page = 20


# Search
@admin.register(Search)
class SearchAdmin(ModelAdmin):
    list_display = ("user", "search_term", "response", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("search_term",)
    ordering = ("-created_at",)
    list_per_page = 20


# SearchTag
@admin.register(SearchTag)
class SearchTagAdmin(ModelAdmin):
    list_display = ("search", "tag_names", "created_at")
    search_fields = ("tag_names",)
    ordering = ("-created_at",)
    list_per_page = 20


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
    list_display = (
        "user",
        "trending",
        "recommendation",
        "update_me",
        "search",
        "community_post",
    )
    list_filter = ("user",)
    search_fields = ("user__username",)
    list_per_page = 20


# Preference
@admin.register(Preference)
class PreferenceAdmin(ModelAdmin):
    list_display = ("user__name", "created_at")
    search_fields = ("user__username",)
    ordering = ("-created_at",)
    list_per_page = 20
