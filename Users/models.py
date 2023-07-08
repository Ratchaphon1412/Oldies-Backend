import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models


ROLE_CHOICES = (
    ('User', 'User'),
    ('Provider', 'Provider')
)

SERVICE_CHOICES = (
    ("Local", "Local"),
    ("Google", "Google"),
    ("Facebook", "Facebook"),
)


class UserProfilesManager(UserManager):
    def get_by_natural_key(self, username: str | None):
        return super().get_by_natural_key(username)


# Create your models here
class UserProfiles(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    profile = models.URLField(max_length=255, blank=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='User')
    service = models.CharField(
        max_length=10, choices=SERVICE_CHOICES, default='Local')
    phone = models.CharField(max_length=10, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    objects = UserProfilesManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=255, blank=True, null=True)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    unitNumber = models.TextField(max_length=255, blank=True, null=True)
    streetNumber = models.TextField(max_length=255, blank=True, null=True)
    address_line_1 = models.TextField(max_length=255, blank=True, null=True)
    address_line_2 = models.TextField(max_length=255, blank=True, null=True)
    city = models.TextField(max_length=255, blank=True, null=True)
    region = models.TextField(max_length=255, blank=True, null=True)
    postal_code = models.TextField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)


class UserAddress(models.Model):
    userID = models.ForeignKey(
        UserProfiles, on_delete=models.SET_NULL, null=True)
    addressID = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True)
    is_default = models.BooleanField(default=False)


class PaymentType(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=255, blank=True, null=True)


class UserPayment(models.Model):
    id = models.AutoField(primary_key=True)
    userID = models.ForeignKey(
        UserProfiles, on_delete=models.SET_NULL, null=True)
    paymentTypeID = models.ForeignKey(
        PaymentType, on_delete=models.SET_NULL, null=True)
    provider = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
