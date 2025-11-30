from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import User, UserDevice, EmailOTP


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin, ImportExportModelAdmin):
    list_display = ("name", "email", "is_staff", "is_active","is_subscribed", "created_at")
    search_fields = ["email", "name"]
    list_filter = ("is_staff", "is_active",)
    list_display_links = ("name", "email")
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
                    # "groups",
                    # "user_permissions",
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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # This block ensures styling for password1 and password2 fields
        if "password1" in form.base_fields:
            form.base_fields["password1"].widget.attrs[
                "class"
            ] = "border border-base-200 bg-white font-medium min-w-20 placeholder-base-400 rounded-default shadow-xs text-font-default-light text-sm focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600 group-[.errors]:border-red-600 focus:group-[.errors]:outline-red-600 dark:bg-base-900 dark:border-base-700 dark:text-font-default-dark dark:group-[.errors]:border-red-500 dark:focus:group-[.errors]:outline-red-500 dark:scheme-dark group-[.primary]:border-transparent px-3 py-2 w-full max-w-2xl "
        if "password2" in form.base_fields:
            form.base_fields["password2"].widget.attrs[
                "class"
            ] = "border border-base-200 bg-white font-medium min-w-20 placeholder-base-400 rounded-default shadow-xs text-font-default-light text-sm focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600 group-[.errors]:border-red-600 focus:group-[.errors]:outline-red-600 dark:bg-base-900 dark:border-base-700 dark:text-font-default-dark dark:group-[.errors]:border-red-500 dark:focus:group-[.errors]:outline-red-500 dark:scheme-dark group-[.primary]:border-transparent px-3 py-2 w-full max-w-2xl "
        return form


@admin.register(UserDevice)
class UserDeviceAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("user", "device_info", "ip_address", "last_used")
    search_fields = ["user__email", "device_info", "ip_address"]
    list_filter = ("last_used",)
    ordering = ("-last_used",)
    list_per_page = 20

    # import_form_class = ImportForm
    export_form_class = ExportForm

    def has_import_permission(self, request):
        return False


# @admin.register(EmailOTP)
# class EmailOTPAdmin(ModelAdmin, ImportExportModelAdmin):
#     list_display = ("user", "otp", "is_verified", "created_at", "attempts")
#     search_fields = ["user__email"]
#     list_filter = ("is_verified", "created_at")
#     ordering = ("-created_at",)
#     list_per_page = 20
#     readonly_fields = ("otp", "created_at")

#     import_form_class = ImportForm
#     export_form_class = ExportForm
