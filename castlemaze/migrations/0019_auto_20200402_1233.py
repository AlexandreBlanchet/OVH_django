# Generated by Django 3.0.5 on 2020-04-02 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('castlemaze', '0018_card_number_of_moves'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='is_tile',
        ),
        migrations.AddField(
            model_name='card',
            name='card_type',
            field=models.CharField(default='tile', max_length=100),
        ),
    ]
