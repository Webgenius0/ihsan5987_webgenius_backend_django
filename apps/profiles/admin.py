from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Profile, FAQ, FAQCategory, ContactUs
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

@admin.register(Profile)
class ProfileAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user", "image")
    search_fields = ["user__email"]
    ordering = ["user__email"]
    list_filter = ["user__is_active"]
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm

@admin.register(FAQCategory)
class FAQCategoryAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]
    ordering = ["name"]
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm

@admin.register(FAQ)
class FAQAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("question", "category")
    search_fields = ["question"]
    ordering = ["category__name"]
    list_filter = ["category"]
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm

@admin.register(ContactUs)
class ContactUsAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("platform", "link")
    search_fields = ["platform"]
    ordering = ["platform"]
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm
    