# Generated by Django 3.0.2 on 2021-04-07 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0020_treeplant_sort'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='treeplant',
            options={'ordering': ('sort',), 'verbose_name_plural': 'TreePlant'},
        ),
    ]
