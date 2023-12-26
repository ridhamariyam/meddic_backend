from rest_framework import generics, permissions, status,filters
from .models import Patient
from .serializer import PatientSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from medcoapp.serializer import UserSerializer
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated


class PatientListView(generics.ListAPIView):
    # 
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientProfileView(generics.RetrieveUpdateAPIView):
    
    serializer_class = PatientSerializer
    # permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    queryset = Patient.objects.all()

class PatientDetailsView(APIView):
    
    def get(self, request, id):
        try:
            patient = Patient.objects.get(account=id)
            serializer = PatientSerializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, id):
        try:
            print(request.data, 'VIEW 31')
            patient = Patient.objects.get(id=id)
            user_serializer = UserSerializer(patient.account, data=request.data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            patient_serializer = PatientSerializer(patient, data=request.data, partial=True)
            if patient_serializer.is_valid():
                patient_serializer.save()
                return Response(patient_serializer.data)
            else:
                errors = {
                    'patient_errors': patient_serializer.errors,
                    'user_errors': user_serializer.errors,
                }
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class Block_user(APIView):
    
    def post(self, request, id):
        
        user = Patient.objects.get(id=id)
        print('patient id-------',user.account.is_active)
        user.account.is_active = False
       
        userData = user.account.save()
        print(userData,'2222222222')
        serializer = PatientSerializer(user)
        return Response(serializer.data, status=200)
        
class Unblock_user(APIView):
    
    def post(self, request, id):
        user = Patient.objects.get(id=id)
        user.account.is_active = True 
        user.account.save()
        serializer = PatientSerializer(user)
        return Response(serializer.data, status=200)
    
    
class PatientSearch(generics.ListAPIView):
    
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['account__first_name', 'id']

    def get_queryset(self):
        query = self.request.query_params.get('search', '')
        
        queryset = Patient.objects.filter(
            Q(account__first_name__icontains=query) |
            Q(id__icontains=query)   
        )

        return queryset
    
