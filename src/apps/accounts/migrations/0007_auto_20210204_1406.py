# Generated by Django 3.0.2 on 2021-02-04 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210202_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='end_position_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Lavozim tugallagan vaqt'),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='start_position_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Lavozim boshlangan vaqt'),
        ),
    ]