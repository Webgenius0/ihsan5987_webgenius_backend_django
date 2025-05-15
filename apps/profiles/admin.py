from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Profile, FAQ, FAQCategory, ContactUs

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ("user", "image")
    search_fields = ["user__email"]
    ordering = ["user__email"]
    list_filter = ["user__is_active"]
    list_per_page = 20

@admin.register(FAQCategory)
class FAQCategoryAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]
    ordering = ["name"]
    list_per_page = 20

@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ("question", "category")
    search_fields = ["question"]
    ordering = ["category__name"]
    list_filter = ["category"]
    list_per_page = 20

@admin.register(ContactUs)
class ContactUsAdmin(ModelAdmin):
    list_display = ("platform", "link")
    search_fields = ["platform"]
    ordering = ["platform"]
    list_per_page = 20
    