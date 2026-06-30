from django.shortcuts import render, redirect, get_object_or_404
# # from paystack import paystack
from django.conf import settings
import requests
from decouple import config
from django.contrib.auth.decorators import login_required
from .models import Payment
from django.core.mail import send_mail
import uuid
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Products, Category, Order, OrderItem, Payment, PurchaseHistories, Cart, CartItem, Review, ReviewReport, BankTransferDetail, Wishlist
from .templatetags.rating_stars import rating_stars
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from decimal import Decimal
from django.db import transaction
from django.contrib.auth.decorators import login_required



# =========== DISPLAY PRODUCT AND OTHER FUNCTIONALITIES ===========
    
@login_required(login_url='login')
def product_list(request):
    products = Products.objects.filter(available=True)
    paginator = Paginator(products, 25)


    page = request.GET.get('page')
    products = paginator.get_page(page)

    return render(request, 'context/product.html', {
        'products': products,
        'paginator': paginator,
        'page': page,
    })


@login_required(login_url='login')
def product_detail(request, product_id, slug):
    product = get_object_or_404(Products, id=product_id, slug=slug)
    return render(request, 'res/product_details.html', {'product': product})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(available=True).select_related('category')
    return render(request, 'res/category.html', {
        'category': category,
        'products': products
    })


# ========== CART SECTION TO BE REVIEW ==========

# @require_POST
@login_required(login_url='login')
def cart_view(request):
    cart_items, _ = Cart.objects.get_or_create(user=request.user)
    # cart_items = cart.items.all()
    total_price = 0
    # for item in cart_items:
        # total_price += item.quantity * item.product.get_price
    return render(request, 'context/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


# @require_POST
@require_http_methods(['GET', 'POST'])
@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')


@require_http_methods(['GET', 'POST'])
@login_required(login_url='login')
def increase_quantity(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = Products.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

# ========== BEGINNING OF INCREMENT AND DECREMENT BUTTON BROUGHT BY ME ==========
def increment_quantity(request, product_id):
  cart_item = Cart.objects.get(product_id=product_id, user=request.user)
  cart_item.quantity += 1
  cart_item.save()
  return redirect('/cart')

def decrement_quantity(request, product_id):
  cart_item = Cart.objects.get(product_id=product_id, user=request.user)
  if cart_item.quantity > 1:
    cart_item.quantity -=1
    cart_item.save()
  else:
    cart_item.delete()
  return redirect('/cart')
# ========== END OF INCREMENT AND DECREMENT BUTTON BROUGHT BY ME ==========

# @require_POST
@login_required(login_url='login')
def decrease_quantity(request, product_id):
    cart_item = CartItem.objects.get(id=product_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def remove_from_cart(request):
    return render(request, 'context/cart.html')



# ========== CHECKOUT FORM SECTION ==========
def checkout_form(request):
    if request.method == "POST":
        request.method

# ========== CHECKOUT SECTION ==========

@require_http_methods(['GET', 'POST'])
@login_required(login_url='login')
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart.items.all())

    order = Order.objects.create(
        user=request.user,
        reference=str(uuid.uuid4()),
        total_amount=cart.total_price()
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            total_price=item.product.price
        )

        cart.items.all().delete()  # clear cart
        return redirect('initialize_payment', order.reference, {
            'order': order
        })
    return render(request, 'context/checkout.html', {
        'total_price': total_price,
    })


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'res/orders.html', {'orders': orders})



#========== WISHLIST SECTION ==========

# @require_POST
@login_required
def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        return {'wishlist_view': wishlist}
    return (request, 'res/wishlist.html', [], {'wishlist': wishlist})


# @require_POST
@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, products=product)

    if not created:
        wishlist.delete()

    return redirect('/products', product_id=product_id)

# @require_POST
@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(
        user=request.user,
        product_id=product_id
    ).delete()

    return redirect('wishlist')


#========== PAYSTACK PAYMENT ==========

@login_required
def initialize_payment(request, reference):
    order = get_object_or_404(Order, reference=reference)   
    if request.method == "POST":
        amount = request.POST.get("amount")
        reference = str(uuid.uuid4())


        payment = Payment.objects.create(
            user=request.user, order=order, 
            amount=order.amount, reference=order.reference,
            email=request.user.email
        )
        context = {
            'payment': payment, 
            'paystack_public_key': settings.config('PAYSTACK_TEST_PUBLIC_KEY')
        }

        return render(request, 'context/pay.html', context)


@login_required
def verify_payment(request, reference):
    payment = get_object_or_404(Payment, reference=reference)

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
      'Authorization': f"Bearer {settings.config('PAYSTACK_TEST_SECRET_KEY')}",
      'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if data['status'] and data['data']['status'] == 'success':
        payment.status = 'success'
        payment.verified = True
        payment.save()
        
        # TO CONFIRM BELOW
        order = payment.order
        order.status = 'paid'
        order.save()

         # 📧 Send Email
        send_mail(
            subject="Payment Successful",
            message=f"Your order {order.reference} was successful!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email]
        )
    else:
        payment.status = 'failed'
        payment.save()
    return redirect('payment_success')



#========== OTHERS FOR HTML SECTION ==========
# <a href="{% url 'cart' %}">Cart</a>
# /product/1/nike-shoe/


#========== COPY AND KEEP CODES ==========
# views.py UPDATED CART FUNCTIONALITY


@require_POST
@login_required
def update_cart_quantity(request):
    product_id = request.POST.get('product_id')
    action = request.POST.get('action')  # "increase" or "decrease"

    cart = get_object_or_404(Cart, user=request.user)

    try:
        with transaction.atomic():  # 🔒 prevents race conditions
            item = CartItem.objects.select_for_update().get(
                cart=cart,
                product_id=product_id
            )

            if action == "increase":
                item.quantity += 1

            elif action == "decrease":
                item.quantity -= 1

                if item.quantity <= 0:
                    item.delete()
                    return JsonResponse({
                        'status': 'removed',
                        'cart_total': cart.total_price()
                    })

            item.save()

            return JsonResponse({
                'status': 'updated',
                'quantity': item.quantity,
                'item_total': item.total_price(),
                'cart_total': cart.total_price()
            })

    except CartItem.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)



       # ✅ 👍 🌐 💳 🛒 ⚙️ 📦 🧱 🚀 ❌ ⚠️ 🔐 🔒



#⚙️ 2. VIEWS (Business Logic)
#✅ Wishlist Views
# views.py

#========== PREVENT OVERSELLING, IF YOUR PRODUCT HAS STOCK ==========
    # if products == "increase":
    #     if item.quantity < item.product.stock:
    #         item.quantity += 1



