# Generated by Django 3.1.7 on 2023-12-01 03:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(
                    max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(
                    blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                 help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('userid', models.AutoField(db_column='UserID',
                 primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('isadmin', models.BooleanField(db_column='isAdmin', default=False)),
                ('admin_verify', models.BooleanField(
                    db_column='Admin_verify', default=False)),
                ('last_signin', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'User',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('auction_id', models.AutoField(
                    db_column='Auction_ID', primary_key=True, serialize=False)),
                ('minimum_price', models.DecimalField(
                    db_column='Minimum_Price', decimal_places=2, max_digits=10)),
                ('ending_time', models.DateTimeField(db_column='Ending_Time')),
            ],
            options={
                'db_table': 'Auction',
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('car_id', models.CharField(db_column='Car_ID',
                 max_length=50, primary_key=True, serialize=False)),
                ('body_style', models.CharField(blank=True,
                 db_column='Body_Style', max_length=50, null=True)),
                ('maker', models.CharField(blank=True,
                 db_column='Maker', max_length=50, null=True)),
                ('model', models.CharField(blank=True,
                 db_column='Model', max_length=50, null=True)),
                ('year', models.IntegerField(blank=True, db_column='Year', null=True)),
                ('location', models.CharField(blank=True,
                 db_column='Location', max_length=100, null=True)),
                ('description', models.TextField(
                    blank=True, db_column='Description', null=True)),
                ('current_status', models.CharField(
                    db_column='Current_Status', default='Pending', max_length=50)),
            ],
            options={
                'db_table': 'Car',
            },
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('shipping_id', models.AutoField(
                    db_column='Shipping_ID', primary_key=True, serialize=False)),
                ('transport_tracking_number', models.CharField(
                    blank=True, db_column='Transport_Tracking_Number', max_length=50, null=True)),
                ('shipping_method', models.CharField(blank=True,
                 db_column='Shipping_Method', max_length=50, null=True)),
                ('shipped_date', models.DateTimeField(
                    blank=True, db_column='Shipped_Date', null=True)),
                ('car', models.ForeignKey(db_column='Car_ID',
                 on_delete=django.db.models.deletion.CASCADE, to='usedCarBidding.car')),
            ],
            options={
                'db_table': 'Shipping',
            },
        ),
        migrations.CreateModel(
            name='Bidding',
            fields=[
                ('bidding_id', models.AutoField(
                    db_column='Bidding_ID', primary_key=True, serialize=False)),
                ('bidding_price', models.DecimalField(
                    db_column='Bidding_Price', decimal_places=2, max_digits=10)),
                ('auction', models.ForeignKey(db_column='Auction_ID',
                 on_delete=django.db.models.deletion.CASCADE, to='usedCarBidding.auction')),
                ('bidder', models.ForeignKey(db_column='Bidder_ID',
                 on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Bidding',
            },
        ),
        migrations.AddField(
            model_name='auction',
            name='car',
            field=models.ForeignKey(
                db_column='Car_ID', on_delete=django.db.models.deletion.CASCADE, to='usedCarBidding.car'),
        ),
        migrations.AddField(
            model_name='auction',
            name='winner',
            field=models.ForeignKey(blank=True, db_column='User_ID', null=True,
                                    on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
