# Generated by Django 3.2.18 on 2023-03-25 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_without_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='without_bid',
        ),
    ]
