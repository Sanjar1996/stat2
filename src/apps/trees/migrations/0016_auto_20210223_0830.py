# Generated by Django 3.0.2 on 2021-02-23 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0015_auto_20210218_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landcategory',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='prepairland',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='prepairlandplan',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='sapling',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='saplinginput',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='saplingoutput',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='saplingplan',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='seed',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='seedinput',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='seedoutput',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='seedplan',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='sprout',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='sproutinput',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='sproutoutput',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='sproutplan',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='treecategory',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='treegroundplanting',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='treegroundplantingplan',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='treeheightreport',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='treeplant',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
        migrations.AlterField(
            model_name='treetypes',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Delete'), (3, 'In Active')], default=1),
        ),
    ]
