# Generated by Django 4.2.3 on 2023-11-02 15:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("travel_api", "0031_tourdayoption_description_ru_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tourdayoption",
            name="date_end",
            field=models.DateTimeField(blank=True, verbose_name="Дата кінця"),
        ),
        migrations.AlterField(
            model_name="tourdayoption",
            name="date_start",
            field=models.DateTimeField(blank=True, verbose_name="Дата початку"),
        ),
        migrations.AlterField(
            model_name="tourdayoption",
            name="description",
            field=models.TextField(blank=True, verbose_name="Опис"),
        ),
        migrations.AlterField(
            model_name="tourdayoption",
            name="description_ru",
            field=models.TextField(blank=True, null=True, verbose_name="Опис"),
        ),
        migrations.AlterField(
            model_name="tourdayoption",
            name="description_uk",
            field=models.TextField(blank=True, null=True, verbose_name="Опис"),
        ),
        migrations.AlterField(
            model_name="tourdayoption",
            name="image_url",
            field=models.URLField(null=True, verbose_name="Зображення"),
        ),
        migrations.AlterField(
            model_name="tourdayoption",
            name="is_landmark",
            field=models.BooleanField(default=False, verbose_name="Визначне місце?"),
        ),
    ]
