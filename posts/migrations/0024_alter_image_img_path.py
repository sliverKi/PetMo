# Generated by Django 4.2 on 2023-04-26 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0023_alter_image_img_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='img_path',
            field=models.ImageField(blank=True, null=True, upload_to='post_images'),
        ),
    ]
