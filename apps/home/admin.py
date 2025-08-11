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
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import (ExportForm, ImportForm)


# Category & Subcategory
@admin.register(Category)
class CategoryAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("category_name", "created_at")
    search_fields = ("category_name",)
    ordering = ("-created_at",)
    list_per_page = 20

    # Import/Export configuration
    import_form_class = ImportForm
    export_form_class = ExportForm


@admin.register(Subcategory)
class SubcategoryAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("subcategory_name", "created_at")
    search_fields = ("subcategory_name",)
    ordering = ("-created_at",)
    list_per_page = 20

    # Import/Export configuration
    import_form_class = ImportForm
    export_form_class = ExportForm


# TopicTag & Topic
@admin.register(TopicTag)
class TopicTagAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("tag_names", "created_at")
    search_fields = ("tag_names",)
    ordering = ("-created_at",)
    list_per_page = 20

    # Import/Export configuration
    import_form_class = ImportForm
    export_form_class = ExportForm


@admin.register(Topic)
class TopicAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("name", "topic_tags", "created_at")
    search_fields = ("name", "topic_tags")
    list_filter = ("topic_tags",)

    # Import/Export configuration
    import_form_class = ImportForm
    export_form_class = ExportForm


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
class RecommendationAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("topic", "category", "subcategory", "headline", "created_at", "last_refresh")
    list_filter = ('category', 'created_at')
    search_fields = ('headline', 'description', 'content')
    ordering = ('-created_at',)
    list_per_page = 20

    # Import/Export configuration
    import_form_class = ImportForm
    export_form_class = ExportForm


@admin.register(UpdateMe)
class UpdateMeAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("topic", "category", "subcategory", "created_at", "interest")
    list_filter = ("created_at", "interest", "category", "subcategory", "topic")
    search_fields = ("short_info", "background_story", "reference_url")
    ordering = ("-created_at",)
    list_per_page = 20

    # Import/Export configuration
    import_form_class = ImportForm
    export_form_class = ExportForm


# KeyWord
@admin.register(KeyWord)
class KeyWordAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("id", "key_words")
    search_fields = ("key_words",)
    list_per_page = 20

    # Import/Export configuration
    import_form_class = ImportForm
    export_form_class = ExportForm


# Trending
@admin.register(Trending)
class TrendingAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("description", "why_trending", "picture_url", "created_at")
    list_filter = ("created_at",)
    search_fields = ("description", "why_trending", "key_points", "outlook")
    list_per_page = 20

    # Import/Export configuration
    import_form_class = ImportForm
    export_form_class = ExportForm


# TrendingUser
@admin.register(TrendingUser)
class TrendingUserAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user", "trending", "clicked_at")
    list_filter = ("clicked_at", "user")
    search_fields = ("user__username",)
    list_per_page = 20

    # Import/Export configuration
    import_form_class = ImportForm
    export_form_class = ExportForm


# RecommendationUser
@admin.register(RecommendationUser)
class RecommendationUserAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user", "recommendation", "clicked_at")
    list_filter = ("clicked_at", "user")
    search_fields = ("user__username",)
    list_per_page = 20

    # Import/Export configuration
    import_form_class = ImportForm
    export_form_class = ExportForm


# Bookmark
@admin.register(Bookmark)
class BookmarkAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user", "content_type", "object_id", "obj", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("user__username", "content_type")
    ordering = ("-created_at",)
    list_per_page = 20

    # Import/Export configuration
    import_form_class = ImportForm
    export_form_class = ExportForm


# Preference
@admin.register(Preference)
class PreferenceAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user__name", "created_at")
    search_fields = ("user__username",)
    ordering = ("-created_at",)
    list_per_page = 20

    # Import/Export configuration
    import_form_class = ImportForm
    export_form_class = ExportForm
