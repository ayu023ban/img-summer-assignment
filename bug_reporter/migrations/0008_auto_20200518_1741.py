# Generated by Django 3.0.5 on 2020-05-18 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug_reporter', '0007_project_githublink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='githublink',
            field=models.URLField(blank=True, null=True),
        ),
    ]
