# Generated by Django 2.2.5 on 2019-11-10 20:01

from django.db import migrations, models
import utils.upload
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20191106_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='document',
            field=models.FileField(null=True, upload_to=utils.upload.task_document_path, validators=[utils.validators.task_document_size, utils.validators.task_document_extension]),
        ),
    ]