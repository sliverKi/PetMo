# Generated by Django 4.2 on 2023-04-24 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_address_latitiude_alter_address_longitude'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='latitiude',
        ),
        migrations.RemoveField(
            model_name='address',
            name='longitude',
        ),
    ]