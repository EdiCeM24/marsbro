from django.shortcuts import render, redirect, get_object_or_404
# # from paystack import paystack
from django.conf import settings
import requests
from django.db.models import Q
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
from .models import Products, Category, Order, OrderItem, Payment, ProductImage, ProductVariant, PurchaseHistories, Cart, CartItem, Review, ReviewReport, BankTransferDetail, Wishlist
from .templatetags.rating_stars import rating_stars
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from decimal import Decimal
from store.models import Product
from store.models import Blog
from django.db import transaction
from django.contrib.auth.decorators import login_required



# =========== DISPLAY PRODUCT AND OTHER FUNCTIONALITIES ===========
    
@login_required(login_url='login')
def product_list(request):
    categories = Category.objects.all()
    products = Products.objects.all().order_by(
        'name', 
        'available', 
        'category',
        'variants',
        'variants__size',
        'variants__color',
    )
   
    # product_avs = Products.objects.filter(available=True)
    paginator = Paginator(products, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

     # Sorting by price
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')    
    sort_by = request.GET.get('sort_by')
    if sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')

    return render(request, 'context/product.html', {
        'page_obj': page_obj,
        'categories': categories,
        'products': products,
    })

# BEST CATEGORY USAGE
@login_required(login_url='login')
def category_products(request, slug):
    category = Category.objects.get(slug=slug)
    # Fetching Products with Variants
    products = Products.objects.select_related(
        "category",
        "subcategory",
        "owner"
    ).prefetch_related(
        "variants__color",
        "variants__size",
        "variants__images",
    ).filter(category=category, available=True)
   
    paginator = Paginator(products, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)    

    return render(request, 'context/product.html', {
        'page_obj': page_obj,
        'category': category,
    })


@login_required(login_url='login')
def product_detail(request, product_id, slug):
    variants = ProductVariant.objects.filter(product_id=product_id)

    images = ProductImage.objects.filter(product_variant__in=variants)
    front_images = images.filter(position='front')
    back_images = images.filter(position='back')
    right_images = images.filter(position='right')
    left_images = images.filter(position='left')
    # other_images = images.filter(position='other')
    # Fetching Products with Variants(optional)
    products = Products.objects.select_related(
        "category",
        "subcategory",
        "owner"
    ).prefetch_related(
        "variants__color",
        "variants__size",
        "variants__images",
    ).get(id=product_id, slug=slug)
     #  Fetch the products
    # product = get_object_or_404(Products, id=product_id, slug=slug)
    return render(request, 'res/product_details.html', {
        'products': products,
        'variants': variants,
        'front_images': front_images,
        'back_images': back_images,
        'right_images': right_images,
        'left_images': left_images,
        # 'other_images': other_images,
    })


def variant_details(request, product_pk, variant_pk):
    variant = ProductVariant.objects.get(product_pk, pk=variant_pk)
    images = variant.images.all()
    return render(request, 'res/variant_details.html', {
        'variant': variant,
        'images': images,
    })


def product_image(request, pk):
    product_img = ProductImage.objects.get(pk=pk)
    return render(request, '', {})


def search_products(request):
    query = request.GET.get('q')
    if query:
        product_cats = Products.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))
    # else:
    #     product_cats = Products.objects.all()
    products = Product.objects.filter(
        Q(topic__icontains=query) | Q(text__icontains=query)
    )
    
    return render(request, 'res/search.html', {
        'product_cats': product_cats,
        'products': products,
    })


def blog_post_detail(request, pk):
    posts = Product.objects.get(pk=pk)
    return render(request, 'home/index.html', {
        'posts':posts
    })

# def category_products(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     # Fetching Products with Variants
#     products = Products.objects.select_related(
#         "category",
#         "subcategory",
#         "owner"
#     ).prefetch_related(
#         "variants__color",
#         "variants__size",
#         "variants__images",
#     )
#     product = category.products.filter(available=True).select_related('category')
#     return render(request, 'includes/category.html', {
#         'category': category,
#         'product': product,
#         'products': products
#     })


# ========== CART SECTION TO BE REVIEW ==========

# @require_POST
@login_required(login_url='login')
def cart_view(request):
    cart_items, _ = Cart.objects.get_or_create(user=request.user)
    # cart_items = cart.items.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items.items.all())
    # for item in cart_items:
        # total_price += item.quantity * item.product.get_price
    return render(request, 'context/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_items.items.count()
    })


# CART COUNT
def get_cart_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        return JsonResponse({'cart_count': cart.products.count()})
    return JsonResponse({ 'cart_count': 0 })


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

    return JsonResponse({'cart_count': cart.items.count()})


@require_http_methods(['GET', 'POST'])
@login_required(login_url='login')
def increase_quantity(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = Products.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()

    return JsonResponse({
        'quantity': cart_item.quantity,
        'cart_count': cart.items.count(),
    })

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
def remove_from_cart(request, product_id):
    try:
        product = Products.objects.get(id=product_id)
    
        cart = Cart.objects.get(user=request.user)
        
        cart.products.remove(product) 
        cart.save()
        return redirect('cart')
    except (product.DoesNotExist, cart.DoesNotExist):
        return redirect('cart')
    



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



