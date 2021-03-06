# Generated by Django 3.0.5 on 2020-04-05 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('castlemaze', '0022_auto_20200403_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='last_cell_played',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_cell_player', to='castlemaze.Cell'),
        ),
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('P', 'Preparation'), ('S', 'Started'), ('B', 'Blue win'), ('R', 'Red win')], default='P', max_length=1),
        ),
    ]
