from django.urls import path
from .views import *
from payments import views

urlpatterns = [
    path('test-payment', views.test_payment),
    path('save_stripe_info/', views.save_stripe_info),
    path('HandleRefund/<int:id>/', HandleRefund.as_view()),
    path('Balance/<int:id>/', Balance.as_view()),
    
   
]
