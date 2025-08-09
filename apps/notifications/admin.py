from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Notification
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm


@admin.register(Notification)
class NotificationAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('sender', 'recipient', 'category', 'notification_type', 'message', 'related_post', 'related_comment', 'image', 'is_read', 'created_at')
    ordering = ('-created_at',)
    list_per_page = 20

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm