# Generated by Django 2.2.2 on 2020-07-04 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20200704_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='notes',
            field=models.CharField(default='', max_length=200, verbose_name='课程公告'),
        ),
    ]
