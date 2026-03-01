from django.urls import path
from . import views


urlpatterns = [
  path(
    'products/', 
    views.products, 
    name='products'
  ),
  path(
    'cart/', 
    views.cart_view, 
    name='cart'
  ),
  path(
    'female_wears/', 
    views.female_wears, 
    name='female_wears'
  ),
  path(
    'men_wears/', 
    views.men_wears, 
    name='men_wears'
  ),
]
