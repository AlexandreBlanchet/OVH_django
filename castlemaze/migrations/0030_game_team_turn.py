# Generated by Django 3.0.5 on 2020-04-09 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('castlemaze', '0029_auto_20200408_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='team_turn',
            field=models.CharField(default='red_team', max_length=100),
        ),
    ]
