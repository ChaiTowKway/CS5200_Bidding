# Generated by Django 3.1.7 on 2023-12-12 22:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usedCarBidding', '0005_comments_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='car_id',
            field=models.ForeignKey(blank=True, db_column='Car_ID', null=True, on_delete=django.db.models.deletion.CASCADE, to='usedCarBidding.car'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='shipping_id',
            field=models.ForeignKey(blank=True, db_column='Shipping_ID', null=True, on_delete=django.db.models.deletion.CASCADE, to='usedCarBidding.shipping'),
        ),
        migrations.AlterField(
            model_name='bidding',
            name='auction_id',
            field=models.ForeignKey(blank=True, db_column='Auction_ID', null=True, on_delete=django.db.models.deletion.CASCADE, to='usedCarBidding.auction'),
        ),
        migrations.AlterField(
            model_name='bidding',
            name='bidder_id',
            field=models.ForeignKey(blank=True, db_column='Bidder_ID', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='car',
            name='seller_id',
            field=models.ForeignKey(blank=True, db_column='Seller_ID', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]