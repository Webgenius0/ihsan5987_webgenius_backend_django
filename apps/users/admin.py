from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ("name", "email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)

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
    ordering = ["email"]