from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Notification
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

@admin.register(Notification)
class NotificationAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('id', 'sender', 'recipient', 'category', 'notification_type', 'message', 'related_post', 'related_comment', 'image', 'is_read', 'created_at')

    import_form_class = ImportForm
    export_form_class = ExportForm