# Generated by Django 3.0.2 on 2021-02-06 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0013_auto_20210201_0413'),
    ]

    operations = [
        migrations.AddField(
            model_name='treetypes',
            name='show_profit',
            field=models.BooleanField(default=False),
        ),
    ]