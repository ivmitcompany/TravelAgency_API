# Generated by Django 4.2.3 on 2023-10-27 18:18

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("travel_api", "0023_alter_orderitem_is_primary_contact_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="code",
            field=models.CharField(unique=True, verbose_name="Номер замовлення"),
        ),
    ]
