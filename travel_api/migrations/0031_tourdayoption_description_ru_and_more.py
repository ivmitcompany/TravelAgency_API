# Generated by Django 4.2.3 on 2023-11-02 15:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("travel_api", "0030_additionaloption_description_ru_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tourdayoption",
            name="description_ru",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tourdayoption",
            name="description_uk",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="tourdayoption",
            name="name_ru",
            field=models.CharField(
                max_length=255,
                null=True,
                validators=[django.core.validators.MinLengthValidator(3)],
                verbose_name="Назва",
            ),
        ),
        migrations.AddField(
            model_name="tourdayoption",
            name="name_uk",
            field=models.CharField(
                max_length=255,
                null=True,
                validators=[django.core.validators.MinLengthValidator(3)],
                verbose_name="Назва",
            ),
        ),
    ]