# Generated by Django 3.0.5 on 2020-05-21 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug_reporter', '0013_auto_20200521_0356'),
    ]

    operations = [
        migrations.AddField(
            model_name='bug',
            name='domain',
            field=models.CharField(blank=True, choices=[('f', 'frontend'), ('b', 'backend'), ('o', 'other')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bug',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('R', 'Resolved'), ('T', 'To be Discussed')], default='P', max_length=100),
            preserve_default=False,
        ),
    ]
