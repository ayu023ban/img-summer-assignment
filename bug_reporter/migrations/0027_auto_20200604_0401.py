# Generated by Django 3.0.6 on 2020-06-04 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bug_reporter', '0026_auto_20200604_0359'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='bug',
            new_name='bugs',
        ),
    ]
