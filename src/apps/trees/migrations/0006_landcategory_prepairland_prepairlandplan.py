# Generated by Django 3.0.2 on 2021-01-19 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('trees', '0005_saplinginput_saplingoutput_seedinput_seedoutput_sproutinput_sproutoutput'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=64)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Delete')], default=1)),
            ],
            options={
                'verbose_name_plural': 'LandCategory',
                'db_table': 'land_category',
            },
        ),
        migrations.CreateModel(
            name='PrepairLandPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateTimeField()),
                ('hectare', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Delete')], default=1)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trees.LandCategory')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Department')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Region')),
            ],
            options={
                'verbose_name_plural': 'PrepairLandPlan',
                'db_table': 'prepair_land_plan',
            },
        ),
        migrations.CreateModel(
            name='PrepairLand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateTimeField()),
                ('hectare', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Delete')], default=1)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trees.LandCategory')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Department')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Region')),
            ],
            options={
                'verbose_name_plural': 'PrepairLand',
                'db_table': 'prepair_land',
            },
        ),
    ]
