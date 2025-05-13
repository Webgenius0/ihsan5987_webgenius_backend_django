from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ("user", "image")
    search_fields = ["user__email"]
    ordering = ["user__email"]
    list_filter = ["user__is_active"]
    list_per_page = 20