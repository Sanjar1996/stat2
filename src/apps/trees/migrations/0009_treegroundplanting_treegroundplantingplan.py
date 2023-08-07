# Generated by Django 3.0.2 on 2021-01-23 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('trees', '0008_auto_20210121_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreeGroundPlantingPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateTimeField()),
                ('desert_plant', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('walnut', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('pistachios', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('nut', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('poplar', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('paulownia', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('other_plants', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Delete')], default=1)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Department')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Region')),
            ],
            options={
                'verbose_name_plural': 'TreeGroundPlantingPlan',
                'db_table': 'tree_ground_planting_plan',
            },
        ),
        migrations.CreateModel(
            name='TreeGroundPlanting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateTimeField()),
                ('desert_plant', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('walnut', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('pistachios', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('nut', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('poplar', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('paulownia', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('other_plants', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Delete')], default=1)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Department')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Region')),
            ],
            options={
                'verbose_name_plural': 'TreePlanting',
                'db_table': 'tree_ground_planting',
            },
        ),
    ]
