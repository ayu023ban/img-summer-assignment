# Generated by Django 3.0.5 on 2020-05-17 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bug_reporter', '0005_auto_20200517_1155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bug',
            old_name='assign_to',
            new_name='assigned_to',
        ),
    ]