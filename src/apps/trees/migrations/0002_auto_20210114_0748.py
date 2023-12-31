# Generated by Django 3.0.2 on 2021-01-14 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='treeplant',
            name='is_show_height',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='treeplant',
            name='is_show_sapling',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='treeplant',
            name='is_show_seed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='treeplant',
            name='is_show_sprouting',
            field=models.BooleanField(default=False),
        ),
    ]
