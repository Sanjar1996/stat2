# Generated by Django 3.0.2 on 2021-02-22 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_userdepartment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userdepartment',
            options={'verbose_name_plural': 'User Departments'},
        ),
        migrations.AlterModelTable(
            name='userdepartment',
            table='user_departments',
        ),
    ]
