# Generated by Django 4.2.3 on 2023-10-24 16:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_api', '0022_order_alter_tour_date_end_alter_tour_date_start_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='is_primary_contact',
            field=models.BooleanField(blank=True, verbose_name='Контакт для звʼязку'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='phone',
            field=models.CharField(blank=True, verbose_name='Номер телефону'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2023, 10, 24, 19, 11, 15, 240695), verbose_name='Дата кінця'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='date_start',
            field=models.DateField(default=datetime.datetime(2023, 10, 24, 19, 11, 15, 240695), verbose_name='Дата почтаку'),
        ),
    ]
