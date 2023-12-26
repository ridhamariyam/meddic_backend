from rest_framework import serializers
from doctor.models import Doctor
from medcoapp.models import *




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = ('id','email', 'first_name', 'last_name', 'password', 'role', 'profile_image', 'is_active', 'phone','date_joined')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        
class LoginSerializer(serializers.ModelSerializer):
    email =serializers.EmailField()
    password = serializers.CharField()
    
    class Meta:
        model = account
        fields = '__all__'

class VarifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        try:
            user = OTP.objects.get(user__email=email)
       
            if user.otp != otp:
                raise serializers.ValidationError('Invalid OTP')

            # Update user verification status
            user_instance = account.objects.get(email=email)
            user_instance.is_active = True
            user.delete()
            user_instance.save()
        except OTP.DoesNotExist:
            raise serializers.ValidationError('Invalid email')

        return data
    
class PasswordResetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = '__all__'