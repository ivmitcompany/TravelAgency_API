# Generated by Django 4.2.3 on 2023-10-19 15:28

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_api', '0014_alter_option_options_alter_order_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='option',
            options={'verbose_name_plural': 'Опції'},
        ),
        migrations.AlterField(
            model_name='tour',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2023, 10, 19, 18, 28, 18, 650489), verbose_name='Дата кінця'),
        ),
        migrations.AlterField(
            model_name='tour',
            name='date_start',
            field=models.DateField(default=datetime.datetime(2023, 10, 19, 18, 28, 18, 650489), verbose_name='Дата почтаку'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='image.png', max_length=255, null=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('aws_url', models.CharField(max_length=255, verbose_name='Посилання на AWS')),
                ('is_main', models.BooleanField(verbose_name='Головне фото')),
                ('time_create', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_update', models.DateTimeField(auto_now=True, null=True)),
                ('tour_image', models.ManyToManyField(related_name='images', to='travel_api.tour')),
            ],
            options={
                'verbose_name': 'Зображення',
                'verbose_name_plural': 'Зображення',
            },
        ),
    ]
