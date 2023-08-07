# Generated by Django 3.0.2 on 2021-02-18 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chorvachilik', '0008_auto_20210217_1326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chorvainputoutput',
            name='docs',
        ),
        migrations.AddField(
            model_name='uploadfile',
            name='output',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chorvachilik.ChorvaInputOutput'),
        ),
    ]
