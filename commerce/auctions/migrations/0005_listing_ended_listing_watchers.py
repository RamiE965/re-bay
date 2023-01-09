# Generated by Django 4.1.4 on 2023-01-04 22:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_imgage_listing_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='ended',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listing',
            name='watchers',
            field=models.ManyToManyField(blank=True, related_name='watchList', to=settings.AUTH_USER_MODEL),
        ),
    ]
