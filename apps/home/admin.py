# from django.contrib import admin
# from unfold.admin import ModelAdmin
# from .models import Notification


# # Register your models here.
# @admin.register(Notification)
# class NotificationAdmin(ModelAdmin):
#     list_display = ("user", "message", "is_read", "created_at")
#     search_fields = ["user__email", "message"]
#     ordering = ["-created_at"]
#     list_filter = ["is_read"]
#     list_per_page = 20
