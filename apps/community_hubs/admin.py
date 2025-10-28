from django.contrib import admin
from unfold.admin import ModelAdmin
# from auditlog.models import LogEntry
from .models import Post, Comment, Like, CommentReport
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import (ExportForm, ImportForm, SelectableFieldsExportForm)


@admin.register(Post)
class PostAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = (
        "title",
        "user",
        "category",
        "is_active",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ["title", "user__email", "user__name", "category__category_name"]
    list_per_page = 20
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
    readonly_fields = ['created_at']

    # Import/Export configuration
    # import_form_class = ImportForm
    export_form_class = ExportForm
    def has_import_permission(self, request):
        return None


@admin.register(Comment)
class CommentAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("post", "user", "text", "is_active", "created_at")
    search_fields = ["post__title", "user__email"]
    list_per_page = 20
    ordering = ["-created_at"]
    list_filter_sheet = True
    list_filter = ("post", "created_at",)

    export_form_class = ExportForm
    def has_import_permission(self, request):
        return None
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('post', 'user')


@admin.register(Like)
class LikeAdmin(ModelAdmin):
    list_display = ("comment", "user", "created_at")
    search_fields = ["comment__post__title", "user__email"]
    list_per_page = 20
    ordering = ["-created_at"]


@admin.register(CommentReport)
class CommentReportAdmin(ModelAdmin):
    list_display = [
        'comment',
        'reporter',
        'reason',
        'message',
        'status',
        'created_at'
    ]
    list_filter = ['status', 'reason']
    search_fields = ['comment__text', 'reporter__username', 'reporter__name']
    readonly_fields = ['created_at']
    list_editable = ['status']
    list_per_page = 20
    ordering = ["-created_at"]

    def save_model(self, request, obj, form, change):
        if obj.status == 'dismissed':
            obj.comment.is_active = False
            obj.comment.save()
        super().save_model(request, obj, form, change)
