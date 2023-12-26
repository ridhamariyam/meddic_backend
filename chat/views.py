from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.response import Response
from .models import *
from .serializer import *
from medcoapp.serializer import UserSerializer
from doctor.serializer import DoctorsListSerializer
from doctor.models import *
from Slot.models import *
from Patient.serializer import *


class PreviousMessagesView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user1 = int(self.kwargs['user1'])
        user2 = int(self.kwargs['user2'])

        thread_suffix = f"{user1}_{user2}" if user1 > user2 else f"{user2}_{user1}"
        thread_name = 'chat_'+thread_suffix
        queryset = DirectMessage.objects.filter(
            thread_name=thread_name
        )
        return queryset


class GetUserDetails(APIView):
    def get(self, request, user_id):
        user = account.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class DoctorList(ListAPIView):
    serializer_class = DoctorsListSerializer
    def get_queryset(self):
        user = int(self.kwargs['id'])
        patient=Patient.objects.get(account__id=user)
        queryset = Doctor.objects.filter(appointment__patient=patient, appointment__mode='chat').distinct()
        print(queryset)
        return queryset
    
class PatientList(ListAPIView):
    serializer_class = PatientSerializer
    def get_queryset(self):
        user = int(self.kwargs['id'])
        doctor=Doctor.objects.get(account__id=user)
        queryset = Patient.objects.filter(appointment__doctor=doctor, appointment__mode='chat').distinct()
        print(queryset)
        return queryset