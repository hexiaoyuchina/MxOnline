# Generated by Django 2.2.2 on 2020-04-29 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200423_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(max_length=11, verbose_name='手机号'),
        ),
    ]
