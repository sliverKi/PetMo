# Generated by Django 4.2 on 2023-04-28 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Free', 'Free'), ('Question', 'Question'), ('Master', 'Master'), ('Review', 'Review'), ('Congrats', 'Congrats'), ('Help', 'Help')], max_length=255)),
            ],
        ),
    ]
