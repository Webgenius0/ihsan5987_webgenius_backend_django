from django.contrib import admin
from unfold.admin import ModelAdmin   
from .models import Post, Comment, Like, CommentReport
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

@admin.register(Post)
class PostAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("id", "title", "user", "category", "created_at")
    search_fields = ["title", "user__email"]
    ordering = ["-created_at"]

    import_form_class = ImportForm
    export_form_class = ExportForm

@admin.register(Comment)
class CommentAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("id", "post", "user", "text", "created_at")
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
    list_display = ("id", "comment", "reporter", "reason", "status", "created_at")
    search_fields = ["comment__post__title", "reporter__email"]
    ordering = ["-created_at"]

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm



