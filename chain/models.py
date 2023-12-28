from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Supplier(MPTTModel):
    """ Модель поставщика """

    FACTORY = 'FR'
    RETAILER = 'RR'
    SOLE_PROPRIETOR = 'SP'

    SUPPLIER_CHOICES = [
        (FACTORY, 'Завод'),
        (RETAILER, 'Розничная сеть'),
        (SOLE_PROPRIETOR, 'Индивидуальный предприниматель'),
    ]

    supplier_type = models.CharField(max_length=20, choices=SUPPLIER_CHOICES, verbose_name='Тип поставщик')
    name = models.CharField(max_length=50, verbose_name='Название')

    email = models.EmailField(verbose_name='Email')
    country = models.CharField(max_length=50, verbose_name='Страна')
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=50, verbose_name='Улица')
    house_number = models.SmallIntegerField(verbose_name='Номер дома')

    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Поставщик')

    debt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Задолженность')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return f'{self.supplier_type} - {self.name}'


class Product(models.Model):
    """ Модель продукта """

    name = models.CharField(max_length=150, verbose_name='Название')
    model = models.CharField(max_length=150, verbose_name='Модель')
    launch_date = models.DateField(verbose_name='Дата выхода')

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Поставщик')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name} - {self.model}'
