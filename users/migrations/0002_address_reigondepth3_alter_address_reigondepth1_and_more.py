# Generated by Django 4.2 on 2023-04-24 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='reigonDepth3',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='reigonDepth1',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='reigonDepth2',
            field=models.CharField(default='', max_length=255),
        ),
    ]
