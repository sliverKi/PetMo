# Generated by Django 4.2 on 2023-04-25 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_remove_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]