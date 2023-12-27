from django.contrib import admin
from django.db import transaction

from chain.models import Supplier, Product
from mptt.admin import MPTTModelAdmin


class SupplierAdmin(MPTTModelAdmin):
    list_display = ('supplier_type', 'name', 'email', 'country', 'city', 'parent', 'debt', 'created')
    list_display_links = ('supplier_type', 'name',)
    list_filter = ('city',)
    mptt_level_indent = 20

    actions = ['clear_debt']

    def clear_debt(self, request, queryset):
        """ Admin action для очистки задолженности перед поставщиком у выбранных объектов """

        with transaction.atomic():
            for supplier in queryset:
                supplier.debt = 0
                supplier.save()

    clear_debt.short_description = "Очистить задолженность перед поставщиком"


admin.site.register(Supplier, SupplierAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'launch_date', 'supplier')
