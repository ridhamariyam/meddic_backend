from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


urlpatterns = [
   path('update/<int:id>', PatientProfileView.as_view(), name='update'),
   path('patient_details/<int:id>', PatientDetailsView.as_view(), name='details'),
   path('patientlist',PatientListView.as_view(),name='Patientlist'),
   path('patientSearch/', PatientSearch.as_view(), name='patient_search'),
   path('Block_user/<int:id>/', Block_user.as_view(), name='Block_user'),
   path('Unblock_user/<int:id>/', Unblock_user.as_view(), name='Unblock_user'),
]

