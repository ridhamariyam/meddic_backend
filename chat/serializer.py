from rest_framework import serializers
from .models import *

class MessageSerializer(serializers.ModelSerializer):
    sender_username=serializers.SerializerMethodField()

    class Meta:
        model=DirectMessage
        fields=['message','sender_username', 'send_at']

    def get_sender_username(self,obj):
        return obj.sender.email
