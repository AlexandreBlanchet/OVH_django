# Generated by Django 3.0.5 on 2020-04-02 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('castlemaze', '0017_auto_20200401_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='number_of_moves',
            field=models.IntegerField(default=0),
        ),
    ]
