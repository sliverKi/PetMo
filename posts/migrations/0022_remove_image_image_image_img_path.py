# Generated by Django 4.2 on 2023-04-26 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0021_alter_image_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image',
        ),
        migrations.AddField(
            model_name='image',
            name='img_path',
            field=models.URLField(blank=True, null=True),
        ),
    ]
