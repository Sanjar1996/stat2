# Generated by Django 3.0.2 on 2021-02-18 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20210216_1223'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ('sort',), 'verbose_name_plural': 'Department'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ('sort',), 'verbose_name_plural': 'Region'},
        ),
    ]
