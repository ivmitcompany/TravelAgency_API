# Generated by Django 4.2.3 on 2023-10-14 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_api', '0005_alter_additionaloption_name_alter_image_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='date_end',
            field=models.DateField(auto_now_add=True, verbose_name='Дата кінця'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='date_start',
            field=models.DateField(auto_now_add=True, verbose_name='Дата почтаку'),
        ),
    ]