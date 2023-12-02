from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    userid = models.AutoField(db_column='UserID', primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    isadmin = models.BooleanField(default=False, db_column='isAdmin')
    admin_verify = models.BooleanField(default=False, db_column='Admin_verify')
    last_signin = models.DateField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'User'
        managed = True

    def __str__(self):
        return self.email


class Car(models.Model):
    car_id = models.CharField(
        db_column='Car_ID', primary_key=True, max_length=50)
    body_style = models.CharField(
        db_column='Body_Style', max_length=50, blank=True, null=True)
    exterior_color = models.CharField(
        db_column='Exterior_Color', max_length=50, blank=True, null=True)
    transmission = models.CharField(
        db_column='Transmission', max_length=50, blank=True, null=True)
    mileage = models.IntegerField(db_column='Mileage', blank=True, null=True)
    engine = models.CharField(
        db_column='Engine', max_length=50, blank=True, null=True)
    title_status = models.CharField(
        db_column='Title_Status', max_length=50, blank=True, null=True)
    make = models.CharField(
        db_column='Make', max_length=50, blank=True, null=True)
    model = models.CharField(
        db_column='Model', max_length=50, blank=True, null=True)
    year = models.IntegerField(db_column='Year', blank=True, null=True)
    drivetrain = models.CharField(
        db_column='Drivetrain', max_length=50, blank=True, null=True)
    location = models.CharField(
        db_column='Location', max_length=100, blank=True, null=True)
    current_status = models.CharField(
        db_column='Current_Status', max_length=50, blank=True, null=True)
    seller_id = models.ForeignKey(
        User, models.DO_NOTHING, db_column='Seller_ID', blank=True, null=True)

    class Meta:
        db_table = 'Car'


class Auction(models.Model):
    auction_id = models.AutoField(db_column='Auction_ID', primary_key=True)
    start_time = models.DateTimeField(
        db_column='Start_Time', blank=True, null=True)
    car_id = models.ForeignKey(
        Car, models.DO_NOTHING, db_column='Car_ID', blank=True, null=True)
    minimum_price = models.DecimalField(
        db_column='Minimum_Price', max_digits=10, decimal_places=2, blank=True, null=True)
    ending_time = models.DateTimeField(
        db_column='Ending_Time', blank=True, null=True)
    additional_info = models.CharField(
        db_column='Additional_Info', max_length=50, blank=True, null=True)
    winner_id = models.ForeignKey(
        User, models.DO_NOTHING, db_column='Winner_id', blank=True, null=True)
    minimum_deposit = models.DecimalField(
        db_column='Minimum_Deposit', max_digits=10, decimal_places=2, blank=True, null=True)
    auction_hold = models.IntegerField(
        db_column='Auction_Hold', blank=True, null=True)
    auction_status = models.CharField(
        db_column='Auction_Status', max_length=50, blank=True, null=True)
    is_verified = models.IntegerField(
        db_column='is_verified', blank=True, null=True)
    payment_id = models.IntegerField(
        db_column='Payment_ID', blank=True, null=True)
    shipping_id = models.ForeignKey(
        'Shipping', models.DO_NOTHING, db_column='Shipping_ID', blank=True, null=True)
    edit_time = models.CharField(
        db_column='Edit_time', max_length=50, blank=True, null=True)
    withdrawn = models.CharField(
        db_column='Withdrawn', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Auction'


class Bidding(models.Model):
    # Field name made lowercase.
    bidding_id = models.AutoField(db_column='Bidding_ID', primary_key=True)
    # Field name made lowercase.
    auction_id = models.ForeignKey(
        Auction, models.DO_NOTHING, db_column='Auction_ID', blank=True, null=True)
    # Field name made lowercase.
    bidder_id = models.ForeignKey(
        'User', models.DO_NOTHING, db_column='Bidder_ID', blank=True, null=True)
    # Field name made lowercase.
    bidding_price = models.DecimalField(
        db_column='Bidding_Price', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'Bidding'


class Shipping(models.Model):
    # Field name made lowercase.
    shipping_id = models.AutoField(db_column='Shipping_ID', primary_key=True)
    # Field name made lowercase.
    transport_tracking_number = models.CharField(
        db_column='Transport_Tracking_Number', max_length=50, blank=True, null=True)
    # Field name made lowercase.
    shipping_method = models.CharField(
        db_column='Shipping_Method', max_length=50, blank=True, null=True)
    # Field name made lowercase.
    delivered_date = models.DateTimeField(
        db_column='Delivered_Date', blank=True, null=True)
    # Field name made lowercase.
    temp_hold = models.CharField(
        db_column='Temp_hold', max_length=50, blank=True, null=True)
    # Field name made lowercase.
    shipping_status = models.CharField(
        db_column='Shipping_Status', max_length=50, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'Shipping'


class Reply(models.Model):
    Reply_ID = models.AutoField(primary_key=True, db_column='Reply_ID')
    ReplyContent = models.CharField(max_length=100, db_column='ReplyContent')
    create_at = models.DateField(db_column='create_at')
    create_by_user_ID = models.IntegerField(db_column='create_by_user_ID')
    create_by_user_Name = models.CharField(
        max_length=100, db_column='create_by_user_Name')
    CommentID = models.ForeignKey(
        'Comments', on_delete=models.CASCADE, db_column='CommentID')

    class Meta:
        # managed = False  # Uncomment this if you don't want Django to manage the table
        db_table = 'reply'


class Comments(models.Model):
    CommentID = models.AutoField(primary_key=True, db_column='CommentID')
    CommenContent = models.CharField(
        max_length=100, db_column='CommenContent')
    create_at = models.DateField(db_column='create_at')
    create_by_user_ID = models.IntegerField(db_column='create_by_user_ID')
    create_by_user_Name = models.CharField(
        max_length=100, db_column='create_by_user_Name')
    auction_id = models.ForeignKey(
        Auction, on_delete=models.CASCADE, db_column='auction_id')

    class Meta:
        # managed = False  # Uncomment this if you don't want Django to manage the table
        db_table = 'Comments'
