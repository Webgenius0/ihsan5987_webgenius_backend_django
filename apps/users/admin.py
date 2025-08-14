from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin, ImportExportModelAdmin):
    list_display = ("name", "email", "is_staff", "is_active",)
    list_filter = ("is_staff", "is_active",)
    list_per_page = 20
    ordering = ("-created_at",)
    fieldsets = (
        (None, {"fields": ("name", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("name", "email", "password", "is_staff", "is_active"),
        }),
    )
    search_fields = ["email", "name"]

    export_form_class = ExportForm

    # disable import
    def has_import_permission(self, request):
        return False
