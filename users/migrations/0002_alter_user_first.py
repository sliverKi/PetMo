# Generated by Django 4.2 on 2023-05-03 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first',
            field=models.BooleanField(default=True),
        ),
    ]
