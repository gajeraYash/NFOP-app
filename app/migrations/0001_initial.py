# Generated by Django 3.1.8 on 2021-04-22 20:54

import NFOP.storages
import app.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadForms',
            fields=[
                ('group', models.CharField(choices=[('MEMB', 'Member'), ('POLI', 'Police')], max_length=4, primary_key=True, serialize=False)),
                ('form', models.FileField(storage=NFOP.storages.FormStorage(), upload_to=app.models.form_storage_path)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Download Form',
                'verbose_name_plural': 'Download Forms',
            },
        ),
        migrations.CreateModel(
            name='FeedbackContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default='', max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField(max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Feedback Contact Request',
                'verbose_name_plural': 'Feedback Contact Requests',
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('link', models.TextField(max_length=500)),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
        migrations.CreateModel(
            name='MailList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=35)),
                ('last_name', models.CharField(max_length=35)),
                ('email', models.CharField(max_length=254)),
            ],
            options={
                'verbose_name': 'MailList Request',
                'verbose_name_plural': 'MailList Requests',
            },
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('UVER', 'Unverified'), ('MEMB', 'Member'), ('POLI', 'Police')], default='UVER', max_length=4)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Status',
                'verbose_name_plural': 'User Status',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_1', models.CharField(max_length=128)),
                ('address_2', models.CharField(blank=True, max_length=128)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=24)),
                ('zip_code', models.CharField(max_length=5)),
                ('phone_number', models.CharField(max_length=14)),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.CreateModel(
            name='PoliceUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.FileField(upload_to=app.models.upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Police Upload',
                'verbose_name_plural': 'Police Uploads',
            },
        ),
        migrations.CreateModel(
            name='MemberUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.FileField(upload_to=app.models.upload_path)),
                ('frontDL', models.ImageField(upload_to=app.models.upload_path)),
                ('backDL', models.ImageField(upload_to=app.models.upload_path)),
                ('carReg', models.ImageField(upload_to=app.models.upload_path)),
                ('date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Member Upload',
                'verbose_name_plural': 'Member Uploads',
            },
        ),
    ]
