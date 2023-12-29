
from django.contrib.auth.models import AbstractUser, BaseUserManager,Permission
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


class account(AbstractUser):

    ROLE_CHOICES = (
        ('user', 'User'),
        ('Doctor', 'Doctor'),
        ('admin', 'Admin')
    )

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.PositiveBigIntegerField(null=True, blank=True)
    role = models.CharField(max_length=30, default='user', choices=ROLE_CHOICES, verbose_name='Role')
    profile_image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    username = models.CharField(max_length=150, unique=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'phone','username']


class OTP(models.Model):
    user = models.OneToOneField(account, on_delete=models.CASCADE)
    otp = models.CharField(max_length=10)
    
class PasswordReset(models.Model):
    user = models.OneToOneField(account, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    

