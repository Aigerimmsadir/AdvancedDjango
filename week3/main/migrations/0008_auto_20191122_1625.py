# Generated by Django 2.2.7 on 2019-11-22 10:25

from django.db import migrations, models
import utils.upload
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_taskcomment_stars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.FileField(null=True, upload_to=utils.upload.avatar_document_path, validators=[utils.validators.task_document_size, utils.validators.avatar_document_extension]),
        ),
    ]
