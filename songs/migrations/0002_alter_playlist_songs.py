# Generated by Django 5.0 on 2023-12-17 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(related_name='playlists', to='songs.song'),
        ),
    ]
