# Generated by Django 3.0.2 on 2021-01-16 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('trees', '0002_auto_20210114_0748'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrowingPlantPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateTimeField()),
                ('count', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Delete')], default=1)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='growing_plan_creator', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='growing_plan_department', to='accounts.Department')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='growing_plant_plan', to='trees.TreePlant')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='growing_plan_region', to='accounts.Region')),
            ],
            options={
                'verbose_name_plural': 'GrowingPlantPlan',
                'db_table': 'growing_plant_plan',
            },
        ),
        migrations.CreateModel(
            name='GrowingPlant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateTimeField()),
                ('count', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Delete')], default=1)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='growing_creator', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='growing_department', to='accounts.Department')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='growing_plant', to='trees.TreePlant')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='growing_region', to='accounts.Region')),
            ],
            options={
                'verbose_name_plural': 'GrowingPlant',
                'db_table': 'growing_plant',
            },
        ),
    ]
