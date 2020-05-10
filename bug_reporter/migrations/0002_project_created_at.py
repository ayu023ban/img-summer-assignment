# Generated by Django 3.0.5 on 2020-05-08 13:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bug_reporter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creation Time'),
            preserve_default=False,
        ),
    ]
