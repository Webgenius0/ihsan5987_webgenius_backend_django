from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from .models import Profile, FAQ, FAQCategory, ContactUs, NotificationSetting, Feedback, AppInfo
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm


@admin.register(Profile)
class ProfileAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user", "image", "premium_user", "created_at")
    search_fields = ["user__email"]
    ordering = ["-created_at"]
    list_filter = ["user__is_active"]
    list_per_page = 20

    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm

    # disable import
    def has_import_permission(self, request):
        return False


@admin.register(FAQCategory)
class FAQCategoryAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]
    ordering = ["name"]
    list_per_page = 20

    # import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm

    def has_import_permission(self, request):
        return False


@admin.register(FAQ)
class FAQAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("category", "question",)
    search_fields = ["question"]
    ordering = ["category__name"]
    list_filter = ["category"]
    list_per_page = 20
    list_filter_sheet = False

    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm

    def has_import_permission(self, request):
        return False


@admin.register(ContactUs)
class ContactUsAdmin(ModelAdmin):
    list_display = ("platform", "link")
    search_fields = ["platform"]
    ordering = ["platform"]
    list_filter = ["platform"]
    list_per_page = 20
    list_filter_sheet = False
    # import_form_class = ImportForm
    # export_form_class = ExportForm
    # selectable_fields_export_form_class = SelectableFieldsExportForm


@admin.register(NotificationSetting)
class NotificationSettingAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user", "comments_on_posts", "like_on_comments", "trending_topics", "my_recommendations", "posts_on_my_interests")
    search_fields = ["user__email", "user__name"]
    ordering = ["-created_at"]
    list_per_page = 20
    list_filter_sheet = False

    # import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm

    def has_import_permission(self, request):
        return False


@admin.register(Feedback)
class FeedbackAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ["user__email"]
    ordering = ["-created_at"]
    list_filter = ["user", "created_at"]
    list_per_page = 20


@admin.register(AppInfo)
class AppInfoAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("id", "job_vacancy_url", "rate_us_url", "privacy_policy_url", "partner_url", "accessibility_url", "community_guidelines_url", "developer_url", "feedback_url", "website_url")
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm
