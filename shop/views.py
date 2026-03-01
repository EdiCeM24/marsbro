from django.shortcuts import render, redirect, get_object_or_404
# from paystack import paystack
from django.conf import settings
from . models import *
from django.http import JsonResponse


def products(request):
  products = Products.objects.all()
  return render(request, 'context/product.html', {
     'products': products,
  })

def men_wears(request):
   return render(request, 'men/wears.html')


def female_wears(request):
   return render(request, 'female/wears.html')

def cart_add(request):
  cart = Cart(request, product_id=id)
  if request.POST.get('action') == 'post':
    product_id = int(request.POST.get('product_id'))
    product = get_object_or_404(products, id=product_id)
    cart.add(product=product)
    response = JsonResponse({'product Name': product.name})
    return response
  

def cart_view(request):
    # cart logic here
    
    paystack =  Paystack(secret_key=settings.PAYSTACK_TEST_SECRET_KEY)
    payment_data = {
      'email': request.user.email,
        'amount': Cart.total_amount * 100,
        'callback_url': 'https://example.com/payment/callback',
    }

    response = paystack.transaction.initialize(payment_data)
    return redirect(response['data'] ['authorization_url'])

    return render(request, 'context/cart.html')


