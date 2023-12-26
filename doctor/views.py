from rest_framework import viewsets
from .models import Doctor,ProfessionalDetails,CertificatesPdf
from medcoapp.serializer import UserSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated 
from medcoapp.models import account
from doctor.serializer import DoctorsListSerializer,ProfessionalDetailsSerializer,CertificatesPdfSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.decorators import action
from django.http import Http404
import fitz  # PyMuPDF
from django.http import HttpResponse
from io import BytesIO
from Slot.models import Appointment
from Patient.models import Patient
from Patient.serializer import *
from Slot.serializer import *

# ================================DOCTORLIST================================================

class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorsListSerializer
    
    
class DoctorUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorsListSerializer
    lookup_field = 'account' 
    
    def get_object(self):
        account_id = self.kwargs.get(self.lookup_field)
        return self.queryset.filter(account__id=account_id).first()
    
# =============================PROFESSIONAL DETAILS=======================================
# class GetProfessionalDetails(generics.ListAPIView):
  
#     def put(self, request, id):
#         try:
#             doctor = Doctor.objects.get(account__id=id)
#             professional_details = ProfessionalDetails.objects.get(doctor=doctor)
            
#             serializer = ProfessionalDetailsSerializer(professional_details, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=400)
#         except Doctor.DoesNotExist:
#             raise Http404("Doctor matching query does not exist")
#         except ProfessionalDetails.DoesNotExist:
#             raise Http404("ProfessionalDetails matching query does not exist")

class GetProfessionalDetails(generics.ListAPIView):
   
    def get(self, request, id):
        print(id, 'dddddd')
        try:
            doctor = Doctor.objects.get(account__id=id)
           
            user, created = ProfessionalDetails.objects.get_or_create(doctor=doctor)
            if created:
                user.save()
            serializer = ProfessionalDetailsSerializer(user)
           
            return Response(serializer.data)
            
        except Doctor.DoesNotExist:
            raise Http404("Doctor matching query does not exist")
        except ProfessionalDetails.DoesNotExist:
            raise Http404("ProfessionalDetails matching query does not exist--------")
    
    def patch(self, request, id):
        try:
            doctor = Doctor.objects.get(account__id=id)
            professional_details, created = ProfessionalDetails.objects.get_or_create(doctor=doctor)
            serializer = ProfessionalDetailsSerializer(professional_details, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except ProfessionalDetails.DoesNotExist:
            return Response({"error": "ProfessionalDetails not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifiedDoctorListView(generics.ListAPIView):
    # queryset = Doctor.objects.filter(is_verified=True)
    serializer_class = DoctorsListSerializer
    def get_queryset(self):
        search_query = self.request.query_params.get('search','')
        verfied_doctors = Doctor.objects.filter( Q(is_verified=True) &
            (Q(specialization__icontains=search_query) |
             Q(account__first_name__icontains=search_query)))
        return verfied_doctors
    
class BlockedDoctorListview(generics.ListAPIView):
    serializer_class = DoctorsListSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('search', '')
        
        blocked_doctors = Doctor.objects.filter(
            Q(account__is_active=False) &
            (Q(specialization__icontains=search_query) |
             Q(account__first_name__icontains=search_query))
        )

        blocked_doctors.update(is_verified=False)

        return blocked_doctors

   
    
class GetDoctordetails(APIView):
   def get(self, request, id):
        user = Doctor.objects.get(id=id)
        serializer = DoctorsListSerializer(user)
        return Response(serializer.data)
    
   def patch(self, request, id):
        print(request.data)
    
        doctor = Doctor.objects.get(id=id)
        user_serializer = UserSerializer(doctor.account, data=request.data, partial=True)
        if user_serializer.is_valid():
            user = user_serializer.save()
            print(user.profile_image,'-------->')
        doctor_serializer = DoctorsListSerializer(doctor, data=request.data, partial=True)
        if doctor_serializer.is_valid():
            doctor = doctor_serializer.save()
            print(doctor,'----->')
            return Response(doctor_serializer.data)
        
        else:
            errors = {
                'patient_errors': doctor_serializer.errors,
                'user_errors': user_serializer.errors,
            }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
class DoctorViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['post'])
    def verify(self, request, id):
        try:
            doctor = Doctor.objects.get(pk=id)
        except Doctor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        print('uytuytrtyu',doctor)

        doctor.is_verified = True
        doctor.save()

        verify_button = '<i class="verified-icon">Verified</i>'
        response_data = {
            'is_verified': doctor.is_verified,
            'verify_button': verify_button,
        }

        return Response(response_data)
    
    

class Block_user(APIView):
    def post(self, request, id):
        user = Doctor.objects.get(id=id)
        user.account.is_active = False 
        user.account.save()
        print(user.account,user.account.is_active)
        serializer = DoctorsListSerializer(user)
        print(user,'hhhhhh')
        return Response(serializer.data, status=200)
        
class Unblock_user(APIView):
    def post(self, request, id):
        user = Doctor.objects.get(id=id)
        user.account.is_active = True 
        user.account.save()
        print(user.account)
        print(user.account.is_active)
        serializer = DoctorsListSerializer(user)
        return Response(serializer.data, status=200)
    
class List_Appointement(generics.ListAPIView):
    queryset = Appointment.objects.all()
    patient = Patient.objects.all()
    patient_serializer = PatientSerializer
    serializer_class = AppointmentSerializer
    def get_patient_name(self, patient_id):
        patient = get_object_or_404(Doctor, id=patient_id)
        print(patient,'jjjjjjj')
        return patient.first_name