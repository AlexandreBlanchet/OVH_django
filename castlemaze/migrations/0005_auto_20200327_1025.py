# Generated by Django 2.2.6 on 2020-03-27 09:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('castlemaze', '0004_auto_20200326_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cell',
            name='card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='castlemaze.Card'),
        ),
        migrations.AlterField(
            model_name='cell',
            name='displayed_card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cell_displayed_card', to='castlemaze.Card'),
        ),
        migrations.AlterField(
            model_name='cell',
            name='x',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9)]),
        ),
        migrations.AlterField(
            model_name='cell',
            name='y',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9)]),
        ),
    ]
