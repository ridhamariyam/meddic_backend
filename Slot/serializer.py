from django.db import models
from doctor.serializer import DoctorsListSerializer
# Create your models here.
from rest_framework import serializers
from .models import Appointment,  AvailableSlot
from Patient.serializer import *

class AvailabilitySerializer(serializers.ModelSerializer):
    doctorr = DoctorsListSerializer()
    class Meta:
        model = AvailableSlot
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorsListSerializer()
    patient = PatientSerializer()
    class Meta:
        model = Appointment
        fields = '__all__'
        
