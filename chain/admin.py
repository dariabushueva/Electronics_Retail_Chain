from django.contrib import admin
from django.db import transaction

from chain.models import Supplier, Product
from mptt.admin import MPTTModelAdmin

from django import forms


class SupplierAdminForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

    def clean_parent(self):
        """ Запрещает создавать завод имеющий поставщика """

        parent = self.cleaned_data.get('parent')
        supplier_type = self.cleaned_data.get('supplier_type')

        if parent and supplier_type == Supplier.FACTORY:
            raise forms.ValidationError('Завод не может иметь поставщика.')

        return parent


class SupplierAdmin(MPTTModelAdmin):
    """ Поставщики в админ-панели """

    list_display = ('supplier_type', 'name', 'email', 'country', 'city', 'parent', 'debt', 'created')
    list_display_links = ('supplier_type', 'name',)
    list_filter = ('city',)
    mptt_level_indent = 20

    form = SupplierAdminForm
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
    """ Продукты в админ-панели """

    list_display = ('name', 'model', 'launch_date', 'supplier')
