# Generated by Django 2.2.6 on 2020-03-17 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payyourdrink', '0007_remove_deal_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='drink',
            name='paid_time',
            field=models.DateTimeField(null=True),
        ),
    ]
