# Generated by Django 3.0.2 on 2021-02-16 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20210212_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='sort',
            field=models.IntegerField(blank=True, null=True, verbose_name='SORT NUMBER'),
        ),
        migrations.AddField(
            model_name='region',
            name='sort',
            field=models.IntegerField(blank=True, null=True, verbose_name='SORT NUMBER'),
        ),
    ]