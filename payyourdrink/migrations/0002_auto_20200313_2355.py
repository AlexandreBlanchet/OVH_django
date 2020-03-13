# Generated by Django 2.2.6 on 2020-03-13 22:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payyourdrink', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='number_of_drinks',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
