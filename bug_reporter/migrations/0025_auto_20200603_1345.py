# Generated by Django 3.0.6 on 2020-06-03 13:45

from django.db import migrations
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('bug_reporter', '0024_auto_20200601_1317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bug',
            options={'ordering': ['-issued_at']},
        ),
        migrations.AlterField(
            model_name='bug',
            name='name',
            field=djrichtextfield.models.RichTextField(blank=True),
        ),
    ]
