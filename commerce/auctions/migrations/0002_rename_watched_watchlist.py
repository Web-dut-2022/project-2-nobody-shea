# Generated by Django 4.0.3 on 2022-04-24 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Watched',
            new_name='Watchlist',
        ),
    ]
