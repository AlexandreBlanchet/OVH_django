# Generated by Django 2.2.6 on 2020-03-28 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('castlemaze', '0010_game_max_number_of_players'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='cell_type',
            field=models.CharField(default='board', max_length=100),
        ),
    ]
