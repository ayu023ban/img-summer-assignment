# Generated by Django 3.0.5 on 2020-04-25 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug_reporter', '0004_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='file',
        ),
        migrations.AddField(
            model_name='file',
            name='image',
            field=models.ImageField(default='dfasff', upload_to='', verbose_name='uploaded image'),
            preserve_default=False,
        ),
    ]
