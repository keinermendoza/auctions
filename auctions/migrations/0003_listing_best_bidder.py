# Generated by Django 3.2.18 on 2023-03-19 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_remove_listing_best_bidder'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='best_bidder',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='properties', to=settings.AUTH_USER_MODEL),
        ),
    ]
