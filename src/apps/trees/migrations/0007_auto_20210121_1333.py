# Generated by Django 3.0.2 on 2021-01-21 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0006_landcategory_prepairland_prepairlandplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='saplingoutput',
            name='out_of_count',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True),
        ),
        migrations.AddField(
            model_name='sproutoutput',
            name='out_of_count',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True),
        ),
    ]
