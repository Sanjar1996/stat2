# Generated by Django 3.0.2 on 2021-02-17 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chorvachilik', '0007_auto_20210206_0529'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='files/')),
            ],
            options={
                'verbose_name_plural': 'UploadFile',
                'db_table': 'upload_file',
            },
        ),
        migrations.AddField(
            model_name='chorvainputoutput',
            name='docs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chorvachilik.UploadFile'),
        ),
    ]
