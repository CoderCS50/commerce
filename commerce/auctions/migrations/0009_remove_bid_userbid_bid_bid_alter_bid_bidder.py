# Generated by Django 4.2.4 on 2023-08-28 01:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_rename_bid_listing_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='userBid',
        ),
        migrations.AddField(
            model_name='bid',
            name='bid',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserBid', to=settings.AUTH_USER_MODEL),
        ),
    ]
