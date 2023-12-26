from rest_framework import generics, permissions
from .models import Appointment,AvailableSlot
from rest_framework.response import Response
from rest_framework import status
from .serializer import AppointmentSerializer, AvailabilitySerializer
from rest_framework.views import APIView
from doctor.models import Doctor
from Patient.models import Patient
import json
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from doctor import views
from doctor.serializer import *
from django.shortcuts import get_object_or_404
from django.utils import timezone



class ListAvailableSlots(APIView):
    def post(self, request, id):
        current_time = str(datetime.now().strftime('%I:%M %p')).lstrip('0')
        date_str = request.data.get('selectedDate')
        doc = Doctor.objects.get(account__id=id)
        datee = datetime.now().date()
       
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        if datee == date:            
            slots = AvailableSlot.objects.filter(
                doctorr=doc, date=date, is_booked=False
            ).order_by('time').exclude(time__lte=current_time)
            
        else:   
            slots = AvailableSlot.objects.filter(
            doctorr=doc, date=date, is_booked=False
            ).order_by('time')

        if slots.exists():
            serializer = AvailabilitySerializer(slots, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(
            data={'message': 'No available slots on the selected date or all slots are in the past!'},
            status=status.HTTP_404_NOT_FOUND
        )
        
        
    
class CreateSlot(APIView):
    def post(self, request):
        try:
            date = request.data.get('date')
            account_id = request.data.get('account')
            time_choice = json.loads(request.data.get('timeChoice'))
           
            print(time_choice)
            doctor = Doctor.objects.get(account__id=account_id)
            for i in time_choice:
                obj, created = AvailableSlot.objects.get_or_create(doctorr=doctor, date=date, time=i)
                if created:
                    obj.save()
            slots = AvailableSlot.objects.filter(
            doctorr=doctor, date=date)
            if slots.exists():
                serializer = AvailabilitySerializer(slots, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)

            return Response(
                data={'message': 'No available slots on the selected date!'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(e)
            return Response(
                data={'message': 'slojte'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
class LIstAllSlot(APIView):
    def get(self,request):
        time_choice = ['09:00-09:30 AM','09:30-10:00 AM','10:00-10:30 AM','10:30-11:00 AM','11:00-11:30 AM','11:30-12:00 AM','12:00-12:30 PM','1:00-1:30 PM', '1:30-2:00 PM', '2:00-2:30 PM','2:30-3:00 PM', '3:00-3:30 PM', '3:30-4:00 PM', '4:00-4:30 PM', '4:30-5:00 PM', '5:00-5:30 PM', '5:30-6:00 PM', '6:00-6:30 PM', '7:00-7:30 PM', '8:00-8:30 PM',
        ]
        
        date = request.GET.get('date')
        account_id = request.GET.get('account')
        doctor = Doctor.objects.get(account__id=account_id)
        added_slots = AvailableSlot.objects.filter(date=date, doctorr = doctor).values_list('time', flat=True)
        added_slots = list(added_slots)
        added_slots_index = []
        for i in added_slots:
            added_slots_index.append(time_choice.index(i))
        
        data = {}
        data['avalailable_slot'] = time_choice
        data['selected_slot'] = added_slots_index
        return Response(data=data)
    
class LIstSlotByTime(APIView):
    def get(self, request):
        
        time_choice = [
            '09:00-09:30 AM', '09:30-10:00 AM', '10:00-10:30 AM', '10:30-11:00 AM',
            '11:00-11:30 AM', '11:30-12:00 AM', '12:00-12:30 PM', '1:00-1:30 PM',
            '1:30-2:00 PM', '2:00-2:30 PM', '2:30-3:00 PM', '3:00-3:30 PM',
            '3:30-4:00 PM', '4:00-4:30 PM', '4:30-5:00 PM', '5:00-5:30 PM',
            '5:30-6:00 PM', '6:00-6:30 PM', '7:00-7:30 PM', '8:00-8:30 PM',
        ]

        
        date = request.GET.get('date')
        account_id = request.GET.get('account')
        doctor = Doctor.objects.get(account__id=account_id)
        added_slots = AvailableSlot.objects.filter(date=date, doctorr = doctor).values_list('time', flat=True)
        added_slots = list(added_slots)
        

        
        current_time = datetime.now().strftime('%I:%M %p')
        current_datetime = datetime.strptime(current_time, '%I:%M %p')
        print(current_time,'111111111')
        print(current_datetime,'22222222')

        
        filtered_slots = [slot for slot in time_choice if self.is_slot_after_current_time(slot, current_datetime)]
        data = {}
        added_slots_index = []
        print(filtered_slots,'filtered')
        print(added_slots)
        for i in added_slots:
            try:
                added_slots_index.append(filtered_slots.index(i))
            except:
                pass
        data['avalailable_slot'] = filtered_slots
        data['selected_slot'] = added_slots_index
        print(added_slots_index)
        return Response(data=data)
    
    def is_slot_after_current_time(self, slot, current_datetime):
        try:
            start_time, end_time_str = slot.split('-')
            _,t = end_time_str.split(' ')
            full_end_time_str = f"{start_time.strip()} {t}"
            start_datetime = datetime.strptime(full_end_time_str, '%I:%M %p')
            return start_datetime >= current_datetime
        except ValueError as e:
            print(f"Error processing slot {slot}: {e}")
            return False
        
        
class BookSlot(generics.CreateAPIView):
    serializer_class = AvailabilitySerializer

    def get(self, request, *args, **kwargs):
        print(request.query_params)
        date = request.query_params.get('date')
        doctor_id = request.query_params.get('doctor')
        time_choice = request.query_params.get('time')
        patient_id = request.query_params.get('patient')
        mode = request.query_params.get('mode')
     
        
        print(date, patient_id, time_choice,doctor_id,mode,'date ahhn tta')

        try:
            available_slot = AvailableSlot.objects.filter(
                time=time_choice, doctorr_id=doctor_id, date=date,
            ).first()
            if available_slot is None:
                return Response(
                    {"error": "oooho"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            available_slot.is_booked = True
            available_slot.save()

        except AvailableSlot.DoesNotExist:
            return Response(
                {"error": "aaahha"},
                status=status.HTTP_400_BAD_REQUEST
            )

        patient = Patient.objects.get(account=patient_id)
        doc = Doctor.objects.get(id=doctor_id)
        appointment = Appointment.objects.create(
            date=date, doctor=doc, time=time_choice, patient=patient, mode=mode
        )
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListAppointement(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    doctor_serializer = DoctorsListSerializer

    def get_queryset(self):
        date_param = self.request.query_params.get('date', None)
        queryset = Appointment.objects.all()

        if date_param:
            queryset = queryset.filter(date=date_param)

        return queryset

    def get_doctor_name(self, doctor_id):
        doctor = get_object_or_404(Doctor, id=doctor_id)
        return doctor.first_name

class CancelAppointmentView(APIView):
    def patch(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update the appointment status to 'Canceled'
        appointment.status = 'Canceled'
        appointment.save()

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Update_appointment_status(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    lookup_field = 'pk'  # Add this line

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ["completed", "missed"]:
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        instance.status = new_status
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)