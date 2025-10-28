from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserDevice, EmailOTP
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin, ImportExportModelAdmin):
    list_display = ("name", "email", "is_staff", "is_active","is_subscribed", "created_at")
    search_fields = ["email", "name"]
    list_filter = ("is_staff", "is_active",)
    list_per_page = 20
    ordering = ("-created_at",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_subscribed",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active', 'is_subscribed'),
        }),
    )
    export_form_class = ExportForm

    # disable import
    def has_import_permission(self, request):
        return False


@admin.register(UserDevice)
class UserDeviceAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user", "device_info", "ip_address", "last_used")
    search_fields = ["user__email", "device_info", "ip_address"]
    list_filter = ("last_used",)
    ordering = ("-last_used",)
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm


@admin.register(EmailOTP)
class EmailOTPAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user", "otp", "is_verified", "created_at", "attempts")
    search_fields = ["user__email"]
    list_filter = ("is_verified", "created_at")
    ordering = ("-created_at",)
    list_per_page = 20
    readonly_fields = ("otp", "created_at")

    import_form_class = ImportForm
    export_form_class = ExportForm
