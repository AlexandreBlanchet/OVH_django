# Generated by Django 2.2.6 on 2020-03-27 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('castlemaze', '0005_auto_20200327_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='clickable',
            field=models.BooleanField(default=False),
        ),
    ]