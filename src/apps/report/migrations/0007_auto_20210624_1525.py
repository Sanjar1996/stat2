# Generated by Django 3.0.2 on 2021-06-24 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0006_report_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportkey',
            name='query_code',
            field=models.TextField(blank=True, null=True, verbose_name='QUERY OR SQL CODE'),
        ),
        migrations.AlterField(
            model_name='reportkey',
            name='value_type',
            field=models.IntegerField(choices=[(1, 'Double'), (2, 'String'), (3, 'QUERY OR SQL')], default=1),
        ),
    ]
