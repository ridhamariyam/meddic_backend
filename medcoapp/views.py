from django.shortcuts import render
from rest_framework import views, permissions
from rest_framework import generics, filters
from .serializer import *
from doctor.serializer import DoctorsListSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
import json
import pyotp
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.db.models import Q
from .models import PasswordReset
from django.core.mail import send_mail
from django.conf import settings
from .serializer import PasswordResetTokenSerializer
import secrets



class LoginApiView(APIView):
    def post(self, request):
        try:
            data = request.data
            print(data, 'himonu')
            serializer = LoginSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']
                print(email, password, "iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
                user = authenticate(email=email, password=password)
                print(user, 'user aahn')

                if user is None:
                    return Response({
                        'message': 'Password or Email is incorrect',
                        'data': {}
                    }, status=status.HTTP_401_UNAUTHORIZED)

                if not user.is_active:
                    return Response({
                        'message': 'user is blocked',
                        'data': {}
                    }, status=status.HTTP_401_UNAUTHORIZED)

                refresh = RefreshToken.for_user(user)
                refresh['role'] = user.role
                refresh['username'] = user.first_name

                # Storing tokens in localStorage
                response_data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

                return Response(response_data, status=status.HTTP_200_OK)

            print(serializer.errors)
            return Response({
                'status': 400,
                'message': serializer.errors,
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal Server Error',
                'data': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
class Register(generics.ListCreateAPIView):
    print('hiii from register')
    queryset=account.objects.all()
    serializer_class = UserSerializer
    # parser_classes = (MultiPartParser, FormParser)
   

class VarifyOTP(APIView):
    def patch(self, request):
        data = request.data
        serializer = VarifyAccountSerializer(data = data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
class doctorsearchlist(generics.ListAPIView):
    
    queryset = Doctor.objects.all()
    serializer_class = DoctorsListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['specialization', 'account__first_name'] 
    
    def get_queryset(self):
        query = self.request.query_params.get('search', '')

        queryset = Doctor.objects.filter(
            Q(specialization__istartswith=query) |
           Q(account__first_name__icontains=query),
            is_verified = True
           
        )
        return queryset


class FetchAllDoctors(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()
    serializer_class = DoctorsListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['specialization', 'account__first_name'] 
    
    def get_queryset(self):
        query = self.request.query_params.get('search', '')

        queryset = Doctor.objects.filter(
            Q(specialization__istartswith=query) |
           Q(account__first_name__icontains=query)
           )
        return queryset
  

# class RequestPasswordResetView(APIView):
#     def send_reset_email(self, to_email, token):
#         subject = 'Password Reset Request'
#         message = f'Click the following link to reset your password: {settings.CORS_ALLOWED_ORIGINS}/change-password/ {token}/'
#         from_email = settings.DEFAULT_FROM_EMAIL

#         send_mail(subject, message, from_email, [to_email])

#     def generate_unique_token(self):
#         return secrets.token_urlsafe(30)

#     def post(self, request):
#         email = request.data.get('email')
#         user = account.objects.filter(email=email).first()

#         if user:
#             token = self.generate_unique_token()
#             PasswordReset.objects.update_or_create(user=user, defaults={'token': token})

#             self.send_reset_email(user.email, token)

#         return Response({'message': 'Password reset link sent if the email exists'}, status=status.HTTP_200_OK)
    
    
# class ChangePasswordView(generics.UpdateAPIView):
#     serializer_class = PasswordResetTokenSerializer
#     queryset = PasswordReset.objects.all()
#     lookup_field = 'token'

#     def update(self, request, *args, **kwargs):
#         token = self.kwargs.get('token')
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)