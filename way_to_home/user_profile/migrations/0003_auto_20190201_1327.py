# Generated by Django 2.1.4 on 2019-02-01 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_userprofile_telegram_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='telegram_id',
            field=models.IntegerField(null=True),
        ),
    ]