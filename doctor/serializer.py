from rest_framework import serializers
from doctor.models import Doctor,ProfessionalDetails,CertificatesPdf
from medcoapp.models import account
from medcoapp.serializer import UserSerializer


class DoctorsListSerializer(serializers.ModelSerializer):
    account = UserSerializer()
    class Meta:
        model = Doctor
        fields = '__all__'


class ProfessionalDetailsSerializer(serializers.ModelSerializer):
    doctor = DoctorsListSerializer()
    
    # professional
    class Meta:
        model = ProfessionalDetails
        fields = '__all__'
        
        
class CertificatesPdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificatesPdf
        fields = '__all__'