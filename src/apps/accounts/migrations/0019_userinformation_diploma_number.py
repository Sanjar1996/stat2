# Generated by Django 3.0.2 on 2021-02-23 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20210222_0501'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='diploma_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Diplom raqami'),
        ),
    ]