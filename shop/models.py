from django.db import models
from django.contrib.auth.models import User
import uuid
from store.validators import *
from django.conf import settings
# import datetime


 
# date_string = "03/01/2026"

# result = datetime.datetime.strptime(date_string, "%m/%d/%Y")

CATEGORY_CHOICES = (
  ('MW', 'Male Wear'),
  ('FW', 'Female Wear'),
  ('AC', 'Accessories'),
  ('MS', 'Men Singlets'),
  ('MB', 'Men Boxers'),
  ('MP', 'Men Pants'),
  ('FS', 'Female Singlets'),
  ('FP', 'Female Pants'),
  ('FB', 'Female Boxers'),
  ('FB', 'Female Bras'),
  ('FS', 'Female Skirts'),
  ('FT', 'Female Tights'),
  ('OT', 'Other'),
)

class Products(models.Model):
  category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
  name = models.CharField(max_length=255, blank=True, null=True)
  product_image = models.ImageField(upload_to='upload', validators=[validationRules])
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock = models.IntegerField()
  discount = models.FloatField(default=0.0)
  desc = models.TextField(max_length=255, blank=True, null=True)
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name
  

class Male_wear(models.Model):
  category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
  name = models.CharField(max_length=255)
  image = models.ImageField(upload_to='stats', validators=[validationRules], blank=True, null=True)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock = models.IntegerField()
  desc = models.TextField() 
  
  def __str__(self):
    return self.name

class Female_wear(models.Model):
  category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
  name = models.CharField(max_length=255)
  image = models.ImageField(upload_to='posts', validators=[validationRules], blank=True, null=True)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock = models.IntegerField()
  desc = models.TextField()

  def __str__(self):
    return self.name
  
  
class Cart(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Cart {self.id} - {self.user.username}"
  

class Wishlist(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  product = models.ForeignKey(Products, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
        return self.product.title

class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  product = models.ForeignKey(Products, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)
  total = models.DecimalField(max_digits=10, decimal_places=2, default=True)
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.quantity} x {self.product.name}'
  

class Order(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  total = models.DecimalField(max_digits=10, decimal_places=2)
  status = models.CharField(max_length=255, choices=[
     ('pending', 'Pending'),
     ('shipped', 'Shipped'),
     ('delivered', 'Delivered'),
     ('cancelled', 'Cancelled')
  ])
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  product = models.ForeignKey(Products, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)
  total_price = models.DecimalField(max_digits=10, decimal_places=2)
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.product.name} X {self.quantity}"


class PurchaseHistorie(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
  puschase_id = models.CharField(max_length=255, default=uuid.uuid4, blank=True, null=True)
  product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True)
  quantity = models.IntegerField(default=1, blank=True, null=True)
  total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
  product_status = models.BooleanField(default=False)
  date = models.DateTimeField(auto_now_add=True)



class Payment(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  payment_method = models.CharField()
  date = models.DateTimeField(auto_now_add=True)


