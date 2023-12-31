# Generated by Django 3.0.2 on 2021-02-23 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20210222_0501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='crop_area',
        ),
        migrations.AlterField(
            model_name='department',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='information',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='nation',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='position',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='region',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
    ]
