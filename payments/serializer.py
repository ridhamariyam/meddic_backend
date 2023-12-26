from rest_framework import serializers
from Patient.serializer import *
from .models import *

class WalletSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Wallet
        fields = '__all__'