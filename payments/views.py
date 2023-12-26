from django.shortcuts import render
from rest_framework import status
from django.http import JsonResponse
import stripe
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from Slot.models import *
from .models import *
from Slot.serializer import *
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from django.db import transaction
from payments.serializer import *

@api_view(['POST'])
def test_payment(request):
    print(request.body)
    price = int(request.query_params.get('price', '')) 
    id = int(request.query_params.get('id', '')) 
    mode = request.query_params.get('mode', '')
    doctor = request.query_params.get('doctor', '')
    date = request.query_params.get('date', '')
    time = request.query_params.get('time', '')
    price *=  100
    print(price)
    session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'Medco',
                        },
                        'unit_amount':price,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f"http://localhost:3000/BookDoctor/{id}?is_success=true&&mode={mode}&&date={date}&&time={time}&&doctor={doctor}",
            cancel_url='http://localhost:3000/BookDoctor/')
    
    return Response(status=status.HTTP_200_OK,data={'url':session.url})


def save_stripe_info(request):
    data = request.data
    email = data['email']   
    payment_method_id = data['payment_method_id']
    
    # creating customer
    customer = stripe.Customer.create(
        email=email, payment_method=payment_method_id
    )
     
    return Response(
        status=status.HTTP_200_OK, 
        data={
            'message': 'Success', 
            'data': {'customer_id': customer.id}
        }
    )
    

@api_view(['GET'])
def save_payment(request):
    pass


class HandleRefund(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    @transaction.atomic
    def post(self, request, id):
        try:
            appointment = Appointment.objects.get(id=id)
            patient = appointment.patient
            user_wallet, _ = Wallet.objects.get_or_create(user=appointment.patient.account)

            refund_amount = self.calculate_refund_amount(appointment)

            user_wallet.balance += refund_amount
            user_wallet.save()

            appointment.status = "Refunded"
            appointment.save()

            return Response(status=status.HTTP_200_OK, data={'message': 'Refund successful'})

        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Appointment not found'})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message': str(e)})

    def calculate_refund_amount(self, appointment):
        doctor_fee = appointment.doctor.fee
        refund_amount = doctor_fee
        
        print(refund_amount, 'doctor fee')
        return refund_amount
    

class Balance(generics.ListAPIView):
    def get(self, request, id):
        try:
            wallet = Wallet.objects.get(user_id=id)
            serializer = WalletSerializer(wallet)
            return Response(serializer.data)
        except Wallet.DoesNotExist:
            return Response({"error": "wallet not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    