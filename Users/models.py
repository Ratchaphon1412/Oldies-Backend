from typing import Optional
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager,PermissionsMixin


ROLE_CHOICES =(
    ('User','User'),
    ('Provider','Provider')
)

class UserProfilesManager(UserManager):
    def get_by_natural_key(self, username: str | None) :
        return super().get_by_natural_key(username)


# Create your models here
class UserProfiles(AbstractBaseUser,PermissionsMixin):
    
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True)
    profile = models.ImageField(upload_to='profile',blank=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='User')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserProfilesManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password']
    
    
    
    