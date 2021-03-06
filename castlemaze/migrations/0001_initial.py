# Generated by Django 2.2.6 on 2020-03-26 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('last_active', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('F', 'First player to move'), ('S', 'Second player to move'), ('W', 'First player wins'), ('L', 'Second player wins'), ('D', 'Draw')], default='F', max_length=1)),
            ],
        ),
    ]
