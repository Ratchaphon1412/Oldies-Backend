import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager,PermissionsMixin


ROLE_CHOICES =(
    ('User','User'),
    ('Provider','Provider')
)

SERVICE_CHOICES = (
    ("Local", "Local"),
    ("Google", "Google"),
    ("Facebook", "Facebook"),
)


class UserProfilesManager(UserManager):
    def get_by_natural_key(self, username: str | None) :
        return super().get_by_natural_key(username)


# Create your models here
class UserProfiles(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True)
    profile = models.URLField(max_length=255,blank=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='User')
    service = models.CharField(max_length=10,choices=SERVICE_CHOICES,default='Local')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    objects = UserProfilesManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    
    
    