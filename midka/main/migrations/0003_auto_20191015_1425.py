# Generated by Django 2.2.5 on 2019-10-15 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20191015_1418'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='existance',
            new_name='existence',
        ),
    ]
