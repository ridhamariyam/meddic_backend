from django.urls import path, include
from .views import *

urlpatterns = [
    path('availableslots/<int:id>/', ListAvailableSlots.as_view()),
    path('createslot/', CreateSlot.as_view()),
    path('listallslot/', LIstAllSlot.as_view()),
    path('ListAppointement/', ListAppointement.as_view()),
    path('LIstSlotByTime/', LIstSlotByTime.as_view()),
    path('updateStatus/<int:pk>/', Update_appointment_status.as_view()),
    path('BookSlot', BookSlot.as_view()),
    # path('appointments/<int:appointment_id>/cancel/', cancel_appointment, name='cancel_appointment'),
    path('cancel_appointment/<int:appointment_id>/', CancelAppointmentView.as_view(), name='cancel-appointment'),
]
