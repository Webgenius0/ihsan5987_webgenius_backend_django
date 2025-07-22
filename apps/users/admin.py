from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

@admin.register(User)
class UserAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("id", "name", "email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    list_per_page = 10
    fieldsets = (
        (None, {"fields": ("name", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("name", "email", "password", "is_staff", "is_active", "groups", "user_permissions"),
        }),
    )
    search_fields = ["email"]
    ordering = ["id"]

    import_form_class = ImportForm
    export_form_class = ExportForm