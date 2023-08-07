# Generated by Django 3.0.2 on 2021-01-29 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_auto_20210128_1536'),
        ('trees', '0011_auto_20210129_0658'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgriculturePlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateTimeField()),
                ('hectare', models.FloatField(blank=True, null=True, verbose_name='Gektar hisobi')),
                ('weight', models.FloatField(blank=True, null=True, verbose_name='wight(tonna)')),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Delete')], default=1)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agriculture_plan_creator', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agriculture_plan_department', to='accounts.Department')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agriculture_plan_region', to='accounts.Region')),
                ('tree_plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agriculture_plan_plant', to='trees.TreePlant')),
                ('tree_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agriculture_plan_tree_type', to='trees.TreeTypes')),
            ],
            options={
                'verbose_name_plural': 'AgriculturePlan',
                'db_table': 'agriculture_plan',
            },
        ),
        migrations.CreateModel(
            name='AgricultureActual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateTimeField()),
                ('hectare', models.FloatField(blank=True, null=True, verbose_name='Gektar hisobi')),
                ('weight', models.FloatField(blank=True, null=True, verbose_name='wight(tonna)')),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Delete')], default=1)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agriculture_actual_creator', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agriculture_actual_department', to='accounts.Department')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agriculture_actual_region', to='accounts.Region')),
                ('tree_plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agriculture_actual_plant', to='trees.TreePlant')),
                ('tree_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agriculture_actual_tree_type', to='trees.TreeTypes')),
            ],
            options={
                'verbose_name_plural': 'AgricultureActual',
                'db_table': 'agriculture_actual',
            },
        ),
    ]
