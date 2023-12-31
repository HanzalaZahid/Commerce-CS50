# Generated by Django 4.2.4 on 2023-10-08 10:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_bids_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created At'),
        ),
        migrations.AddField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created At'),
        ),
        migrations.AddField(
            model_name='listing',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created At'),
        ),
    ]
