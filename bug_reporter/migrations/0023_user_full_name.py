# Generated by Django 3.0.6 on 2020-06-01 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug_reporter', '0022_auto_20200531_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]