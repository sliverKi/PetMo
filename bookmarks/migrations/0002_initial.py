# Generated by Django 4.2 on 2023-05-01 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
        ('bookmarks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='posts.post'),
        ),
    ]
