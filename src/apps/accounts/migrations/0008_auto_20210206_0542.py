# Generated by Django 3.0.2 on 2021-02-06 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210204_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='passport_number',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Pasport seriya va raqami qachon kim tomonidan berilganligi'),
        ),
    ]
