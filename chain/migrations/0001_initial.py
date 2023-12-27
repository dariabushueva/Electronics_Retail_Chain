# Generated by Django 5.0 on 2023-12-27 12:40

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_type', models.CharField(choices=[('FR', 'Завод'), ('RR', 'Розничная сеть'), ('SP', 'Индивидуальный предприниматель')], max_length=20, verbose_name='Тип поставщик')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('country', models.CharField(max_length=50, verbose_name='Страна')),
                ('city', models.CharField(max_length=50, verbose_name='Город')),
                ('street', models.CharField(max_length=50, verbose_name='Улица')),
                ('house_number', models.SmallIntegerField(verbose_name='Номер дома')),
                ('debt', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Задолженность перед поставщиком')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chain.supplier', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('model', models.CharField(max_length=150, verbose_name='Модель')),
                ('launch_date', models.DateField(verbose_name='Дата выхода')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chain.supplier', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
    ]