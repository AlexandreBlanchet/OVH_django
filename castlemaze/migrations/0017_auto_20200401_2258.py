# Generated by Django 3.0.5 on 2020-04-01 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('castlemaze', '0016_auto_20200331_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='open_bottom',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='card',
            name='open_left',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='card',
            name='open_right',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='card',
            name='open_top',
            field=models.BooleanField(default=False),
        ),
    ]
