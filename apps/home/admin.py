from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import (
    Category,
    Subcategory,
    # TopicTag,
    Topic,
    SearchOption,
    SearchHistory,
    Search,
    SearchTag,
    Recommendation,
    # KeyWord,
    Trending,
    # TrendingUser,
    # RecommendationUser,
    Bookmark,
    Preference,
    UpdateMe
)
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget

from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from django_celery_beat.admin import ClockedScheduleAdmin as BaseClockedScheduleAdmin
from django_celery_beat.admin import CrontabScheduleAdmin as BaseCrontabScheduleAdmin
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django_celery_beat.admin import PeriodicTaskForm, TaskSelectWidget

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)


class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    pass


# @admin.register(SolarSchedule)
# class SolarScheduleAdmin(ModelAdmin):
#     pass


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    pass


# Category & Subcategory
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("category_name", "created_at")
    search_fields = ("category_name",)
    ordering = ("created_at",)
    list_per_page = 20


@admin.register(Subcategory)
class SubcategoryAdmin(ModelAdmin):
    list_display = ("subcategory_name", "created_at")
    search_fields = ("subcategory_name",)
    ordering = ("created_at",)
    list_per_page = 20


# TopicTag & Topic
# @admin.register(TopicTag)
# class TopicTagAdmin(ModelAdmin):
#     list_display = ("tag_names", "created_at")
#     search_fields = ("tag_names",)
#     ordering = ("-created_at",)
#     list_per_page = 20


@admin.register(Topic)
class TopicAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("-created_at",)
    list_per_page = 20
    list_filter_sheet = False

    # import_form_class = ImportForm
    export_form_class = ExportForm

    def has_import_permission(self, request):
        return False


# Option
@admin.register(SearchOption)
class SearchOptionAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("keyword", "search_tag", "category", "subcategory", "created_at")
    search_fields = ("search_tag__tag_name", "keyword", "category", "subcategory")
    list_filter = ("category", "subcategory")
    ordering = ("-created_at",)
    list_per_page = 20

    # import_form_class = ImportForm
    export_form_class = ExportForm

    def has_import_permission(self, request):
        return False


# Search
@admin.register(Search)
class SearchAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("topic", "category", "subcategory", "further_key_words", "created_at")
    list_filter = ("category", "subcategory", "topic")
    search_fields = ("category", "subcategory", "topic")
    ordering = ("-created_at",)
    list_per_page = 20

    # import_form_class = ImportForm
    export_form_class = ExportForm

    def has_import_permission(self, request):
        return False


# SearchTag
@admin.register(SearchTag)
class SearchTagAdmin(ModelAdmin):
    list_display = ("tag_name", "created_at")
    search_fields = ("tag_name",)
    ordering = ("-created_at",)
    list_per_page = 20

    # import_form_class = ImportForm
    # export_form_class = ExportForm


@admin.register(SearchHistory)
class SearchHistoryAdmin(ModelAdmin):
    list_display = ("user__email", "search_term", "is_delete", "created_at")
    list_filter = ("user__email", "is_delete")
    search_fields = ("user__email", "search_term")
    ordering = ("-created_at",)
    list_per_page = 20


# Recommendation
@admin.register(Recommendation)
class RecommendationAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("topic", "category", "headline", "created_at", "last_refresh")
    list_filter = ('category', 'created_at')
    search_fields = ('headline', 'description', 'content')
    ordering = ('-created_at',)
    list_per_page = 20

    # import_form_class = ImportForm
    export_form_class = ExportForm

    def has_import_permission(self, request):
        return False


@admin.register(UpdateMe)
class UpdateMeAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("topic", "category", "subcategory", "created_at", "interest")
    list_filter = ("created_at", "interest", "category", "subcategory", "topic")
    search_fields = ("short_info", "background_story", "reference_url")
    ordering = ("-created_at",)
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm

    # optimize queryset
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("category", "subcategory", "topic")
        return qs


# @admin.register(KeyWord)
# class KeyWordAdmin(ModelAdmin, ImportExportModelAdmin):
#     list_display = ("id", "key_words")
#     search_fields = ("key_words",)
#     ordering = ("id",)
#     list_per_page = 20

#     import_form_class = ImportForm
#     export_form_class = ExportForm


# Trending
@admin.register(Trending)
class TrendingAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("category", "subcategory", "picture_url", "created_at")
    list_filter = ("created_at", "category", "subcategory")
    search_fields = ("description", "key_points")
    list_display_links = ("category", "subcategory")
    ordering = ("-created_at",)
    list_per_page = 20

    # import_form_class = ImportForm
    export_form_class = ExportForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("category", "subcategory")
        return qs

    def has_import_permission(self, request):
        return False

    def picture_url(self, obj):
        if obj.picture_url:
            return format_html('<a href="{0}" target="_blank">{0}</a>', obj.picture_url)
        return "-"

# TrendingUser
# @admin.register(TrendingUser)
# class TrendingUserAdmin(ModelAdmin, ImportExportModelAdmin):
#     list_display = ("user", "trending", "clicked_at")
#     list_filter = ("clicked_at", "user")
#     search_fields = ("user__username",)
#     ordering = ("-clicked_at",)
#     list_per_page = 20

#     import_form_class = ImportForm
#     export_form_class = ExportForm


# RecommendationUser
# @admin.register(RecommendationUser)
# class RecommendationUserAdmin(ModelAdmin, ImportExportModelAdmin):
#     list_display = ("user", "recommendation", "clicked_at")
#     list_filter = ("clicked_at", "user")
#     search_fields = ("user__username",)
#     ordering = ("-clicked_at",)
#     list_per_page = 20

#     import_form_class = ImportForm
#     export_form_class = ExportForm


# Bookmark
@admin.register(Bookmark)
class BookmarkAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user__email", "content_type", "object_id", "created_at")
    list_filter = ("user__email", "content_type", "object_id")
    search_fields = ("user__email", "content_type", "object_id")
    ordering = ("-created_at",)
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm


# Preference
@admin.register(Preference)
class PreferenceAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user__name", "created_at")
    search_fields = ("user__username",)
    ordering = ("-created_at",)
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm
