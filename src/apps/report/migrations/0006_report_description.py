# Generated by Django 3.0.2 on 2021-04-26 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0005_report_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='description',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]
