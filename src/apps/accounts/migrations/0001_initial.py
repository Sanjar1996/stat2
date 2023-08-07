# Generated by Django 3.0.2 on 2021-01-14 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('mid_name', models.CharField(blank=True, max_length=255, null=True)),
                ('temporary_work', models.CharField(blank=True, max_length=255, null=True, verbose_name='Вақтинча меҳнатга лаёқатсизлиги (соҳада ишлаган вақтида неча маротаба)')),
                ('crop_area', models.FloatField(blank=True, null=True, verbose_name='Ekin joyi')),
                ('status', models.IntegerField(choices=[(1, 'New'), (2, 'Active'), (3, 'Deleted')], default=1)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Delete')], default=1)),
            ],
            options={
                'verbose_name_plural': 'Information',
                'db_table': 'information',
            },
        ),
        migrations.CreateModel(
            name='Nation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Delete')], default=1)),
            ],
            options={
                'verbose_name_plural': 'Nation',
                'db_table': 'nation',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=120)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Delete')], default=1)),
            ],
            options={
                'verbose_name_plural': 'Position',
                'db_table': 'position',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Delete')], default=1)),
            ],
            options={
                'verbose_name_plural': 'Region',
                'db_table': 'region',
            },
        ),
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('year_of_graduation', models.DateTimeField(blank=True, null=True, verbose_name='OTM tugatgan yili')),
                ('name_of_graduation', models.CharField(blank=True, max_length=255, null=True, verbose_name='Oliy talim nomi va joyi')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Tugilgan yili')),
                ('birth_place', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tugilgan joyi')),
                ('specialization', models.CharField(blank=True, max_length=120, null=True, verbose_name='Mutahasislik')),
                ('passport_number', models.CharField(blank=True, max_length=120, null=True, verbose_name='Pasport seriya va raqami qachon kim tomonidan berilganligi')),
                ('start_position_date', models.DateTimeField(verbose_name='Lavozim boshlangan vaqt')),
                ('end_position_date', models.DateTimeField(verbose_name='Lavozim tugallagan vaqt')),
                ('gender', models.CharField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Mixin')], default=1, max_length=24)),
                ('residence_address', models.CharField(blank=True, max_length=120, null=True, verbose_name='Yashash joyi MFY')),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('academic_degree', models.CharField(blank=True, max_length=255, null=True, verbose_name='ilmiy daraja,unvon,diplom raqami')),
                ('tour', models.CharField(blank=True, max_length=255, null=True, verbose_name='Qaysi chet ellarda bolgansiz qachon qayerda')),
                ('favorite_party', models.CharField(blank=True, max_length=120, null=True, verbose_name="Qaysi partiya a'zosi")),
                ('languages', models.CharField(blank=True, max_length=255, null=True, verbose_name='Qaysi chet tillarini bilasiz qay darajada')),
                ('family_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='oilangiz nech kishidan iborat')),
                ('people_deputy', models.CharField(blank=True, max_length=255, null=True, verbose_name='Xalq deputatat azosimi agar bolsa toliq malumot')),
                ('state_award', models.CharField(blank=True, max_length=255, null=True, verbose_name='Давлат мукофотлари билан тақдирланганми (қанақа)')),
                ('cripple', models.CharField(choices=[(1, 'Yoq'), (2, 'Xa')], default=1, max_length=24, verbose_name='Ногиронлиги')),
                ('military_service', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ҳарбий хизматга муносабати ва ҳарбий унвони')),
                ('judicial', models.CharField(blank=True, max_length=255, null=True, verbose_name='Суд жавобгарлигига тортилган бўлсангиз, қачон ва нима учун')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_information', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'UserInformation',
                'db_table': 'user_information',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Delete')], default=1)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_region', to='accounts.Region')),
            ],
            options={
                'verbose_name_plural': 'Department',
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('address1', models.CharField(blank=True, max_length=255, null=True)),
                ('address2', models.CharField(blank=True, max_length=255, null=True)),
                ('town', models.CharField(blank=True, max_length=50, null=True)),
                ('street', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('home_number', models.CharField(blank=True, max_length=50, null=True)),
                ('home_no', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.IntegerField(choices=[(1, 'Home'), (2, 'Office')])),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Deleted')])),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Region')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
                'db_table': 'address',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_department', to='accounts.Department'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.Group'),
        ),
        migrations.AddField(
            model_name='user',
            name='information',
            field=models.ForeignKey(blank=True, max_length=120, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_information', to='accounts.Information', verbose_name="Ma'lumotu"),
        ),
        migrations.AddField(
            model_name='user',
            name='national',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_national', to='accounts.Nation'),
        ),
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_position', to='accounts.Position', verbose_name='Lavozimi'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]