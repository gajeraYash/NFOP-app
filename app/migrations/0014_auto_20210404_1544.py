# Generated by Django 3.1.6 on 2021-04-04 19:44

import app.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20210404_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policeupload',
            name='form',
            field=models.FileField(upload_to=app.models.upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]
