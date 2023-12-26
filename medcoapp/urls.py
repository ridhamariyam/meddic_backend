from django.urls import path
from .views import *

urlpatterns = [
    # path('doctor/', Doctorlist.as_view())
    path('login/', LoginApiView.as_view()),
    
    
   
    path('register/',Register.as_view(),name='register'),
    path('varify/', VarifyOTP.as_view(), name='varify'),
    path('find_doctors/', doctorsearchlist.as_view(), name='finddoctors'),
    path('FetchAllDoctors/', FetchAllDoctors.as_view(), name='FetchAllDoctors'),
    
   
]