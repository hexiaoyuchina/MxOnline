# Generated by Django 2.2.2 on 2020-04-29 20:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CoureseComment',
            new_name='CourseComments',
        ),
        migrations.RenameModel(
            old_name='UserFavoriate',
            new_name='UserFavorite',
        ),
    ]
