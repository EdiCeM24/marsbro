







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


