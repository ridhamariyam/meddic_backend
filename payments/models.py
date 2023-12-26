from django.db import models
from medcoapp.models import account

class Wallet(models.Model):
    user = models.OneToOneField(account, on_delete=models.CASCADE,null=True,blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)