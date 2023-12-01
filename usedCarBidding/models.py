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
    maker = models.CharField(
        db_column='Maker', max_length=50, blank=True, null=True)
    model = models.CharField(
        db_column='Model', max_length=50, blank=True, null=True)
    year = models.IntegerField(db_column='Year', blank=True, null=True)
    location = models.CharField(
        db_column='Location', max_length=100, blank=True, null=True)
    description = models.TextField(
        db_column='Description', blank=True, null=True)
    current_status = models.CharField(
        db_column='Current_Status', max_length=50, default='Pending')

    class Meta:
        db_table = 'Car'


class Auction(models.Model):
    auction_id = models.AutoField(db_column='Auction_ID', primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, db_column='Car_ID')
    minimum_price = models.DecimalField(
        db_column='Minimum_Price', max_digits=10, decimal_places=2)
    ending_time = models.DateTimeField(db_column='Ending_Time')
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='User_ID', blank=True, null=True)

    class Meta:
        db_table = 'Auction'


class Bidding(models.Model):
    bidding_id = models.AutoField(db_column='Bidding_ID', primary_key=True)
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, db_column='Auction_ID')
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column='Bidder_ID')
    bidding_price = models.DecimalField(
        db_column='Bidding_Price', max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Bidding'


class Shipping(models.Model):
    shipping_id = models.AutoField(db_column='Shipping_ID', primary_key=True)
    transport_tracking_number = models.CharField(
        db_column='Transport_Tracking_Number', max_length=50, blank=True, null=True)
    shipping_method = models.CharField(
        db_column='Shipping_Method', max_length=50, blank=True, null=True)
    shipped_date = models.DateTimeField(
        db_column='Shipped_Date', blank=True, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, db_column='Car_ID')

    class Meta:
        db_table = 'Shipping'
