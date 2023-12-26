from django.core.mail import send_mail
import random
from django.conf import settings
from .models import account, OTP
from doctor.models import Doctor
from Patient.models import Patient
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from .models import PasswordReset

@receiver(post_save, sender=account)
def sent_email_via_otp(sender, instance, created, **kwargs):
    if created:
        subject = 'Your account varification email'
        otp = random.randint(1000, 9999)
        message = f'Your otp is {otp}'
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, [instance.email])
        user = account.objects.get(email = instance.email)
        user_otp = OTP.objects.create(user = user, otp = otp)
        user_otp.save()



@receiver(post_save, sender=account)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'Doctor':
            Doctor.objects.create(account = instance)
        if instance.role == 'user':
            Patient.objects.create(account = instance)
        
