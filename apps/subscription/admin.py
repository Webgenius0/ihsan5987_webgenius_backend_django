from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Package, Subscription
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm

@admin.register(Package)
class PackageAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('id', 'name', 'price', 'description', 'interval', 'stripe_product_id', 'stripe_price_id', 'discount', 'discount_price', 'is_active',)
    list_display_links = ('id', 'name',)

    import_form_class = ImportForm
    export_form_class = ExportForm

@admin.register(Subscription)
class SubscriptionAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('id', 'user', 'package', 'start_date', 'end_date', 'stripe_subscription_id', 'is_active')
    list_display_links= ('id', 'user', 'package',)

    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_fields_export_form_class = SelectableFieldsExportForm