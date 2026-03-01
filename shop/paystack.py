from paystack import Paystack
from django.shortcuts import redirect
from django.conf import settings
from . models import *
import json
import requests


def checkout(payload):
  headers = {
    'Authorization': f"Bearer {settings.PAYSTACK_TEST_ACCESS_KEY}",
    'Content-Type': 'application/json'
  }

  response = requests.post(
    'https://api.paystack.co/transaction/initialize', 
    headers=headers, 
    data=json.dumps(payload)
  )
  response_data = response.json()
  if response_data['status']:
    return response_data['data']['authorization_url']
  else:
    return response_data['message']
  




# def payment_callback(request):
#   paystack = Paystack(secret_key=settings.PAYSTACK_TEST_SECRET_KEY)
#   reference = request.GET.get('reference')
#   response = paystack.transaction.verify(reference)
#   if response ['data']['status'] == 'success':
#     # Update payment status and cart startus
#     payment = Payment.objects.get_404(reference=reference)
#     Payment.payment_status = 'success'
#     payment.save()

#     Cart.status = 'paid'
#     Cart.save()
#   return redirect('payment_success')  
