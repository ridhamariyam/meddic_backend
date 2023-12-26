from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


urlpatterns = [
   path('doctors/', DoctorListView.as_view(), name='doctor-list'),
   path('doctor_details/<int:id>', GetDoctordetails.as_view(), name='get-doctor-details'),
   path('doctor_update/<int:account>', DoctorUpdateView.as_view(), name='get-doctor-update'),
   path('verified_doctors/',VerifiedDoctorListView.as_view(),name='Verified_Doctor_List'),
   path('blocked_doctors/',BlockedDoctorListview.as_view(),name='blocked_Doctor_List'),
   path('List_Appointement/',List_Appointement.as_view(),name='List_Appointement'),

   path('verify_doctor/<int:id>/verify/', DoctorViewSet.as_view({'post': 'verify'})),
   path('Block_user/<int:id>/', Block_user.as_view(), name='Block_user'),
   path('Unblock_user/<int:id>/', Unblock_user.as_view(), name='Unblock_user'),
   path('Professionaldetails/<int:id>/', GetProfessionalDetails.as_view(), name='Professionaldetails'),
   # path('DocUpdateView/<int:id>/', DocUpdateView.as_view(), name='DocUpdateView'),
   # path('getCertificate/<int:id>/', getCertificate.as_view(), name='getCertificate'),
   
   
  
   
]

