from django.urls import path
from . import views


urlpatterns = [
    # ----------------------------
    # PRODUCT ROUTES
    # ----------------------------
    path('products/', views.product_list, name='products'),
    path('product/<int:product_id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_products, name='product_category'),

    # ----------------------------
    # CART ROUTES
    # ----------------------------
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    # path('increment/<int:product_id>/', views.increment_quantity, name='increment_quantity'),
    # path('decrement/<int:product_id>/', views.decrement_quantity, name='decrement_quantity'),

    # ----------------------------
    # ORDER / CHECKOUT
    # ----------------------------
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    # path('orders/<int:id>/', views.order_detail, name='order_detail'),

    # ----------------------------
    # REVIEWS
    # ----------------------------
    # path('review/add/', views.add_review, name='add_review'),
    # path('review/remove/', views.remove_review, name='remove_review'),

    # ----------------------------
    # WISHLIST
    # ----------------------------
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # ----------------------------
    # Payment
    # ----------------------------
    path('pay/<str:reference>/', views.initialize_payment, name='initialize_payment'),
    path('verify/<str:reference>/', views.verify_payment, name='verify_payment'),
]



# urls.py
#path('cart/update/', views.update_cart_quantity, name='update_cart_quantity'),


# urlpatterns = [
#   path(
#     'products/', 
#     views.products, 
#     name='products'
#   ),
#   path(
#     '<slug:category_slug>/',
#     views.products, 
#     name='product_by_category'
#   ),
#   path(
#     'product/<int:pk>/<slug:slug>/',
#     views.product_view, 
#     name='product'
#   ),
#   path(
#     'add-to-cart/<int:product_id>/', 
#     views.add_to_cart, 
#     name='add_to_cart'
#   ),
#   path(
#     'cart/', 
#     views.cart, 
#     name='cart'
#   ),
#   path(
#     'add-to-wishlist/<int:product_id>/',
#     views.add_to_wihlist,
#     name='add_to_wishlist'
#   ),
#   path(
#     'increase-quantity/<int:order_item_id>/', 
#     views.increase_quantity, 
#     name='increase-quantity'
#   ),
#   path(
#     'decrease-quantity/<int:order_item_id>/', 
#     views.decrease_quantity, 
#     name='decrease-quantity'
#   ),
#   path(
#     'checkout/', 
#     views.checkout, 
#     name='checkout'
#   ),
#   path(
#     'female_wears/', 
#     views.female_wears, 
#     name='female_wears'
#   ),
#   path(
#     'men_wears/', 
#     views.men_wears, 
#     name='men_wears'
#   ),
#   path(
#     'rate-product/', 
#     views.rate_product, 
#     name='rate_product'
#   ),
#   path(
#     'remove-rating/', 
#     views.remove_rating, 
#     name='remove_rating'
#   ),
#   path(
#     'report-review/', 
#     views.report_review, 
#     name='report_review'
#   ),
# ]
