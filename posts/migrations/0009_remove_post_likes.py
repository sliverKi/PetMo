# Generated by Django 4.2 on 2023-04-29 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]