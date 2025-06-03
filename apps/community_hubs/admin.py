from django.contrib import admin
from unfold.admin import ModelAdmin   
from .models import Post, Comment, Like, CommentReport
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

@admin.register(Post)
class PostAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("id", "title", "content", "category", "user", "created_at")
    search_fields = ["title", "user__email"]
    ordering = ["-created_at"]

    import_form_class = ImportForm
    export_form_class = ExportForm

@admin.register(Comment)
class CommentAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("id", "post", "user", "text", "is_active", "created_at")
    search_fields = ["post__title", "user__email"]
    ordering = ["-created_at"]

    import_form_class = ImportForm
    export_form_class = ExportForm

@admin.register(Like)
class LikeAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("comment", "user", "created_at")
    search_fields = ["comment__post__title", "user__email"]
    ordering = ["-created_at"]

    import_form_class = ImportForm
    export_form_class = ExportForm

@admin.register(CommentReport)
class CommentReportAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['id', 'comment', 'reporter', 'reason', 'message', 'status', 'created_at']
    list_filter = ['status', 'reason']
    search_fields = ['comment__text', 'reporter__username', 'reporter__name']
    readonly_fields = ['created_at']

    # Optional: Make status editable directly from the list view
    list_editable = ['status']

    # Optional: Add ordering by status and created_at
    ordering = ['-created_at']

    def save_model(self, request, obj, form, change):
        if obj.status == 'dismissed':
            obj.comment.is_active = False
            obj.comment.save()
        super().save_model(request, obj, form, change)


    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm



