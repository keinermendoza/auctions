# Generated by Django 3.2.18 on 2023-03-19 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='best_bidder',
        ),
    ]
