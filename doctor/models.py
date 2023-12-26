from django.db import models
from medcoapp.models import account




class Doctor(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    account = models.OneToOneField(account, on_delete=models.CASCADE, related_name='doctor_profile')
    fee = models.BigIntegerField(default=600)
    specialization = models.CharField(max_length=255)
    experiance = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,blank=True,null=True)
    qualification = models.CharField(max_length=100,blank=True,null=True)
    language = models.CharField(max_length=100,blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    bio=models.TextField(default=True)
    
    def __str__(self) -> str:
        return self.account.email
    

class ProfessionalDetails(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic_address = models.CharField(max_length=255, blank=True, null=True)
    graduation_year = models.CharField(max_length=4, blank=True, null=True)
    medical_license = models.CharField(max_length=20, blank=True, null=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    consultation_types = models.CharField(max_length=255, blank=True, null=True)
    

class CertificatesPdf(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    certificate_image = models.FileField(upload_to='certificates/', blank=True, null=True)