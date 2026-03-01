from django.contrib import admin
from . models import *


class ProductsAdmin(admin.ModelAdmin):
  list_display = ('name', 'category', 'price', 'product_image', 'stock', 'discount')
  search_fields = ('name', 'category')
  list_filter = ('category',)
  # prepopulated_fields = {'slug': ('name',)}


class Female_wearAdmin(admin.ModelAdmin):
  list_display = ('name', 'category', 'price', 'image', 'stock')
  search_fields = ('name', 'category')
  list_filter = ('category',)
  # prepopulated_fields = {'slug': ('name',)}


class Male_wearAdmin(admin.ModelAdmin):
  list_display = ('name', 'category', 'price', 'image', 'stock')
  search_fields = ('name', 'category')
  list_filter = ('category',)
  # prepopulated_fields = {'slug': ('name',)}


class CartAdmin(admin.ModelAdmin):
  list_display = ('user', )


class WishlistAdmin(admin.ModelAdmin):
  list_display = ('user', )

class CartItemAdmin(admin.ModelAdmin):
  list_display = ('cart', 'product', 'quantity', 'total')


class OrderAdmin(admin.ModelAdmin):
  list_display = ('user', 'created_at', 'status')


class OrderItemAdmin(admin.ModelAdmin): 
  list_display = ('order', 'product', 'quantity', 'total_price')


class PurchaseHistorieAdmin(admin.ModelAdmin):
  list_display = ('user', 'product', 'product_id', 'quantity', 'total_price', 'date')


class PaymentAdmin(admin.ModelAdmin):
  list_display = ('user', 'amount', 'payment_method', 'date')  



admin.site.register(Products, ProductsAdmin)

admin.site.register(Male_wear, Male_wearAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Female_wear, Female_wearAdmin)

admin.site.register(Wishlist, WishlistAdmin)

admin.site.register(CartItem, CartItemAdmin)

admin.site.register(Order, OrderAdmin)

admin.site.register(OrderItem, OrderItemAdmin)

admin.site.register(PurchaseHistorie, PurchaseHistorieAdmin)

admin.site.register(Payment, PaymentAdmin)


