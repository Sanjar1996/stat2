# Generated by Django 3.0.2 on 2021-02-20 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chorvachilik', '0012_merge_20210220_0551'),
    ]

    operations = [
        migrations.AddField(
            model_name='chorvachilik',
            name='profit',
            field=models.BooleanField(default=False),
        ),
    ]
