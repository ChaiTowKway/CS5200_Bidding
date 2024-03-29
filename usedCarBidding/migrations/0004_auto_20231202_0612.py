# Generated by Django 3.1.7 on 2023-12-02 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usedCarBidding', '0003_auto_20231201_0716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipping',
            name='car_id',
        ),
        migrations.AddField(
            model_name='bidding',
            name='bidder_id',
            field=models.ForeignKey(blank=True, db_column='Bidder_ID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bidding',
            name='bidding_price',
            field=models.DecimalField(blank=True, db_column='Bidding_Price', decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterModelTable(
            name='bidding',
            table='Bidding',
        ),
    ]
