# Generated by Django 3.1.3 on 2023-08-21 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlinecourse', '0005_auto_20230819_1140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='selected_id',
            new_name='is_selected',
        ),
    ]
