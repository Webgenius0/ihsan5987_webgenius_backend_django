from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from .models import Profile, FAQ, FAQCategory, ContactUs, NotificationSetting
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

@admin.register(Profile)
class ProfileAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user", "image", "premium_user",)
    search_fields = ["user__email"]
    ordering = ["user__email"]
    list_filter = ["user__is_active"]
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm

@admin.register(FAQCategory)
class FAQCategoryAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]
    ordering = ["name"]
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm

@admin.register(FAQ)
class FAQAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("question", "category")
    search_fields = ["question"]
    ordering = ["category__name"]
    list_filter = ["category"]
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm

@admin.register(ContactUs)
class ContactUsAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("platform", "link")
    search_fields = ["platform"]
    ordering = ["platform"]
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm

@admin.register(NotificationSetting)
class NotificationSettingAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user", "comment_on_posts", "like_on_comments", "trending_topics", "my_recommendations", "posts_on_my_interests")
    search_fields = ["user__email"]
    ordering = ["user__email"]
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm
