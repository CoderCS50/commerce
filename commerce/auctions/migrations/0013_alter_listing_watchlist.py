# Generated by Django 4.2.4 on 2023-08-28 23:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_bid_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlistUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
