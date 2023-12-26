from django.db import models
from doctor.models import Doctor
from Patient.models import Patient

class Appointment(models.Model):

    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('Refunded','Refunded'),
        ('Missed', 'Missed'),
    ]
    

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='Confirmed')
    mode = models.CharField(blank=True, null=True,max_length=100)
    
    
class AvailableSlot(models.Model):
    TIME_CHOICES = [
        ('09:00-09:30 AM', '09:00-09:30 AM'),
        ('09:30-10:00 AM', '09:30-10:00 AM'),
        ('10:00-10:30 AM', '10:00-10:30 AM'),
        ('10:30-11:00 AM', '10:30-11:00 AM'),
        ('11:00-11:30 AM', '11:00-11:30 AM'),
        ('11:30-12:00 AM', '11:30-12:00 AM'),
        ('12:00-12:30 PM', '12:00-12:30 PM'),
        ('1:00-1:30 PM', '1:00-1:30 PM'),
        ('1:30-2:00 PM', '1:30-2:00 PM'),
        ('2:00-2:30 PM', '2:00-2:30 PM'),
        ('2:30-3:00 PM', '2:30-3:00 PM'),
        ('3:00-3:30 PM', '3:00-3:30 PM'),
        ('3:30-4:00 PM', '3:30-4:00 PM'),
        ('4:00-4:30 PM', '4:00-4:30 PM'),
        ('4:30-5:00 PM', '4:30-5:00 PM'),
        ('5:00-5:30 PM', '5:00-5:30 PM'),
        ('5:30-6:00 PM', '5:30-6:00 PM'),
        ('6:00-6:30 PM', '6:00-6:30 PM'),
        ('7:00-7:30 PM', '7:00-7:30 PM'),
        ('8:00-8:30 PM', '8:00-8:30 PM'),
    ]   
    doctorr = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=True)
    date = models.DateField(blank=True, null=True)
    time = models.CharField(choices=TIME_CHOICES,max_length=100)
    is_booked = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.doctorr.account.first_name} {self.time}"