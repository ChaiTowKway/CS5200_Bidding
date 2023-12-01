# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Auction(models.Model):
    auction_id = models.AutoField(db_column='Auction_ID', primary_key=True)  # Field name made lowercase.
    start_time = models.DateTimeField(db_column='Start_Time', blank=True, null=True)  # Field name made lowercase.
    car_id = models.ForeignKey('Car', models.DO_NOTHING, db_column='Car_ID', blank=True, null=True)  # Field name made lowercase.
    minimum_price = models.DecimalField(db_column='Minimum_Price', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ending_time = models.DateTimeField(db_column='Ending_Time', blank=True, null=True)  # Field name made lowercase.
    additional_info = models.CharField(db_column='Additional_Info', max_length=50, blank=True, null=True)  # Field name made lowercase.
    winner_id = models.ForeignKey('User', models.DO_NOTHING, db_column='Winner_id', blank=True, null=True)  # Field name made lowercase.
    minimum_deposit = models.DecimalField(db_column='Minimum_Deposit', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    auction_hold = models.IntegerField(db_column='Auction_Hold', blank=True, null=True)  # Field name made lowercase.
    auction_status = models.CharField(db_column='Auction_Status', max_length=50, blank=True, null=True)  # Field name made lowercase.
    is_verified = models.IntegerField(db_column='is_verified',blank=True, null=True)
    payment_id = models.IntegerField(db_column='Payment_ID', blank=True, null=True)  # Field name made lowercase.
    shipping_id = models.ForeignKey('Shipping', models.DO_NOTHING, db_column='Shipping_ID', blank=True, null=True)  # Field name made lowercase.
    edit_time = models.CharField(db_column='Edit_time', max_length=50, blank=True, null=True)  # Field name made lowercase.
    withdrawn = models.CharField(db_column='Withdrawn', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'Auction'


class Bidder(models.Model):
    bidder_id = models.OneToOneField('User', models.DO_NOTHING, db_column='Bidder_ID', primary_key=True)  # Field name made lowercase.
    minimum_deposit = models.DecimalField(db_column='Minimum_Deposit', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    max_price = models.DecimalField(db_column='Max_Price', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    auto_bid = models.IntegerField(db_column='Auto_Bid', blank=True, null=True)  # Field name made lowercase.
    is_verified = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'Bidder'


class Bidding(models.Model):
    bidding_id = models.AutoField(db_column='Bidding_ID', primary_key=True)  # Field name made lowercase.
    auction_id = models.ForeignKey(Auction, models.DO_NOTHING, db_column='Auction_ID', blank=True, null=True)  # Field name made lowercase.
    bidder_id = models.ForeignKey('User', models.DO_NOTHING, db_column='Bidder_ID', blank=True, null=True)  # Field name made lowercase.
    bidding_price = models.DecimalField(db_column='Bidding_Price', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'Bidding'


class Car(models.Model):
    car_id = models.CharField(db_column='Car_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    body_style = models.CharField(db_column='Body_Style', max_length=50, blank=True, null=True)  # Field name made lowercase.
    exterior_color = models.CharField(db_column='Exterior_Color', max_length=50, blank=True, null=True)  # Field name made lowercase.
    transmission = models.CharField(db_column='Transmission', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mileage = models.IntegerField(db_column='Mileage', blank=True, null=True)  # Field name made lowercase.
    engine = models.CharField(db_column='Engine', max_length=50, blank=True, null=True)  # Field name made lowercase.
    title_status = models.CharField(db_column='Title_Status', max_length=50, blank=True, null=True)  # Field name made lowercase.
    make = models.CharField(db_column='Make', max_length=50, blank=True, null=True)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=50, blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    drivetrain = models.CharField(db_column='Drivetrain', max_length=50, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=100, blank=True, null=True)  # Field name made lowercase.
    current_status = models.CharField(db_column='Current_Status', max_length=50, blank=True, null=True)  # Field name made lowercase.
    seller_id = models.ForeignKey('User', models.DO_NOTHING, db_column='Seller_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'Car'


# class Message(models.Model):
#     seller = models.OneToOneField('User', models.DO_NOTHING, db_column='Seller_ID', primary_key=True)  # Field name made lowercase.
#     bidder = models.ForeignKey('User', models.DO_NOTHING, db_column='Bidder_ID')  # Field name made lowercase.
#     message_content = models.TextField(db_column='Message_Content', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         # managed = False
#         db_table = 'Message'
#         unique_together = (('seller', 'bidder'),)


class Seller(models.Model):
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='UserID', primary_key=True)  # Field name made lowercase.
    first_car_release_date = models.DateField(blank=True, null=True, db_column='first_car_release_date')

    class Meta:
        # managed = False
        db_table = 'Seller'


class Shipping(models.Model):
    shipping_id = models.AutoField(db_column='Shipping_ID', primary_key=True)  # Field name made lowercase.
    transport_tracking_number = models.CharField(db_column='Transport_Tracking_Number', max_length=50, blank=True, null=True)  # Field name made lowercase.
    shipping_method = models.CharField(db_column='Shipping_Method', max_length=50, blank=True, null=True)  # Field name made lowercase.
    delivered_date = models.DateTimeField(db_column='Delivered_Date', blank=True, null=True)  # Field name made lowercase.
    temp_hold = models.CharField(db_column='Temp_hold', max_length=50, blank=True, null=True)  # Field name made lowercase.
    shipping_status = models.CharField(db_column='Shipping_Status', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'Shipping'


class User(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    register_date = models.DateField(db_column='Register_Date', blank=True, null=True)  # Field name made lowercase.
    last_signin = models.DateField(db_column='Last_Signin', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)  # Field name made lowercase.
    isadmin = models.IntegerField(db_column='isAdmin', blank=True, null=True)  # Field name made lowercase.
    admin_verify = models.IntegerField(db_column='Admin_verify', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'User'
