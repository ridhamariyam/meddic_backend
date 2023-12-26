from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


urlpatterns = [
    path("user-previous-chats/<int:user1>/<int:user2>/", PreviousMessagesView.as_view()),
    path('getuserdetails/<int:user_id>/',GetUserDetails.as_view(),name='UserDetails'),
    path('getchatlist/<int:id>', DoctorList.as_view()),
    path('getpatientchatlist/<int:id>', PatientList.as_view())
]

