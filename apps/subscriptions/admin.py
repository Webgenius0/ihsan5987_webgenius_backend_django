from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Plan, Subscription
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

@admin.register(Plan)
class PlanAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ["id",'name', 'price', 'duration_months', 'stripe_price_id']
    readonly_fields = ['stripe_price_id']

    import_form_class = ImportForm
    export_form_class = ExportForm

@admin.register(Subscription)
class SubscriptionAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("id", "user", "plan", "stripe_subscription_id", "is_active", "start_date", "end_date")

    import_form_class = ImportForm
    export_form_class = ExportForm