# Generated by Django 2.2.6 on 2020-03-27 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('castlemaze', '0006_cell_clickable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cell',
            name='card_orientation',
        ),
        migrations.RemoveField(
            model_name='deck',
            name='current_card_index',
        ),
        migrations.AddField(
            model_name='game',
            name='player_turn',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cards', models.ManyToManyField(to='castlemaze.Card')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(to='castlemaze.Player'),
        ),
    ]