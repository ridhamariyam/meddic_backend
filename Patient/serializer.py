from rest_framework import serializers
from .models import Patient
from medcoapp.serializer import UserSerializer

class PatientSerializer(serializers.ModelSerializer):
    account = UserSerializer()
    class Meta:
        model = Patient
        fields = '__all__'

    