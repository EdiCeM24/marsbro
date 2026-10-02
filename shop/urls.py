from django.urls import path
from . import views


urlpatterns = [
    # ----------------------------
    # PRODUCT ROUTES
    # ----------------------------
    path('products/', views.product_list, name='products'),
    path('product/<int:product_id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('products/<product_pk>/<variants>/<variant_pk>/', views.variant_details, name='variant_details'),
    

    # ----------------------------
    # SEARCH ROUTES
    # ----------------------------
    path('search/', views.search_products, name='search_products'),
    path('post/<int:pk>/', views.blog_post_detail, name='blog_post_detail'),
    
    # ----------------------------
    # CART ROUTES
    # ----------------------------
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/add/', views.get_cart_count, name='get_cart_count'),
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


