from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from .models import Profile, FAQ, FAQCategory, ContactUs, NotificationSetting, Feedback, AppInfo
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

@admin.register(Profile)
class ProfileAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("id", "user", "image", "premium_user",)
    search_fields = ["user__email"]
    ordering = ["created_at"]
    list_filter = ["user__is_active"]
    list_per_page = 10

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm
    ordering = ["id"]

@admin.register(FAQCategory)
class FAQCategoryAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("id", "name",)
    search_fields = ["name"]
    ordering = ["name"]
    list_filter = ["name"]
    list_per_page = 10

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm
    ordering = ["id"]

@admin.register(FAQ)
class FAQAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("question", "category")
    search_fields = ["question"]
    ordering = ["category__name"]
    list_filter = ["category"]
    list_per_page = 10

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm
    ordering = ["id"]

@admin.register(ContactUs)
class ContactUsAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("platform", "link")
    search_fields = ["platform"]
    ordering = ["platform"]
    list_filter = ["platform"]
    list_per_page = 10

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm

    ordering = ["id"]

@admin.register(NotificationSetting)
class NotificationSettingAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("id" ,"user", "comments_on_posts", "like_on_comments", "trending_topics", "my_recommendations", "posts_on_my_interests")
    search_fields = ["user__email"]
    ordering = ["-created_at"]
    list_filter = ["user"]
    list_per_page = 10

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm\
    
    ordering = ["id"]

@admin.register(Feedback)
class FeedbackAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("id", "user", "search", "content_snippet", "rating", "created_at")
    search_fields = ["user__email", "content"]
    ordering = ["-created_at"]
    list_filter = ["user", "rating", "created_at"]
    list_per_page = 10

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm

    ordering = ["id"]

    def content_snippet(self, obj):
        return (obj.content[:50] + "...") if len(obj.content) > 50 else obj.content
    content_snippet.short_description = "Content"

@admin.register(AppInfo)
class AppInfoAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("id","job_vacancy_url", "rate_us_url", "privacy_policy_url", "partner_url", "accessibility_url", "community_guidelines_url", "developer_url", "feedback_url", "website_url")
    list_per_page = 10

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm