import uuid
from django.db import models
from django.contrib.auth.models import User
from store.validators import validationRules
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# import datetime
from decimal import Decimal
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator


User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)

    parent = models.ForeignKey(
      'self',
      on_delete=models.CASCADE,
      null=True,
      blank=True,
      related_name='children'
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)
    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )

    name = models.CharField(max_length=150)
    slug = models.SlugField()

    class Meta:
        unique_together = ("category", "slug")

    def __str__(self):
        return self.name  
    
    class Meta:
        verbose_name_plural = "SubCategories"


class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )
    name = models.CharField(max_length=255, default='')
    product_image = models.ImageField(upload_to='upload', validators=[validationRules])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    slug = models.SlugField(max_length=255)
    brand = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    desc = models.TextField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def get_price(self):
        if self.discount > 0:
            return self.price - (self.price * self.discount / Decimal(100))
        return self.price

    class Meta:
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        return reverse("products", kwargs=[self.id, self.slug])  # "slug":self.slug

    def __str__(self):
        return self.name
    

class Color(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='variants_color', blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    hex_code = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True, related_name='variants_size')
    name = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class ProductVariant(models.Model):

    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE
    )

    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE
    )

    # image = models.ImageField(upload_to="pictures", blank=True, null=True)
    sku = models.CharField(max_length=50, unique=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.color.name} - {self.size.name}" 


class ProductImage(models.Model):

    FRONT = "front"
    BACK = "back"
    LEFT = "left"
    RIGHT = "right"
    OTHER = "other"

    POSITION_CHOICES = (
        (FRONT, "Front"),
        (BACK, "Back"),
        (LEFT, "Left"),
        (RIGHT, "Right"),
        (OTHER, "Other"),
    )

    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="data", validators=[validationRules])

    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES
    )

    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product_variant.product.name} - {self.position} - Image"


class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(
      validators=[MinValueValidator(1), MaxValueValidator(5)],
      choices=[
      (1, '1 Star'),
      (2, '2 Stars'),
      (3, '3 Stars'),
      (4, '4 Stars'),
      (5, '5 Stars')
    ])

class Meta:
    unique_together = ('product', 'user')

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    self.product.update_average_rating()

def update_average_rating(self):
    avg = self.product.review.aggregate(avg=Avg('rating'))['avg'] or 0
    self.average_rating()
    self.product.save()


class ReviewReport(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    reason = models.TextField()
     
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products, through='CartItem')
    removed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user}"
    
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())    

    def get_total(self):
        return sum(item.get_total_price() for item in self.items.all())
    class Meta:
        verbose_name_plural = "Cart"
        constraints = [
          models.UniqueConstraint(fields=['user'], name='unique_user_cart')
      ]

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', )
    product = models.ForeignKey(Products, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def get_total_price(self):
        return self.quantity * self.product
        # super().save(*args, **kwargs)  # Ensure the model saves after calculating total price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=[
      ('pending', 'Pending'),
      ('paid', 'Paid'),
      ('shipped', 'Shipped'),
      ('delivered', 'Delivered'),
      ('cancelled', 'Cancelled')
    ], default='pending')
    shipping_address = models.CharField(max_length=255, default='')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=True)
    reference = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        return sum(item.get_total_price() for item in self.items.all())

    def __str__(self):
        return f"Order {self.ordered} - {self.user}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return self.quantity * self.total_price

    def __str__(self):
        return f"{self.product.name} X {self.quantity}"


class PurchaseHistories(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purschase_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Purchase Histories"


class Payment(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    CARD = 'card'
    BANK_TRANSFER = 'bank_transfer'
    PAYSTACK = 'paystack'

    METHOD_CHOICES = (
      (CARD, _('Card Payment')),
      (BANK_TRANSFER, _('Bank Transfer')),
      (PAYSTACK, _('Paystack')),
    )

    # PAYMENT STATUSES
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'

    STATUS_CHOICES = (
      (PENDING, _('Pending')),
      (COMPLETED, _('Completed')),
      (FAILED, _('Failed')),
      (REFUNDED, _('Refunded')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Using the choices here
    payment_method = models.CharField(
      max_length=20, choices=METHOD_CHOICES, default=CARD
    )
    status = models.CharField(
      max_length=20, choices=STATUS_CHOICES, default=PENDING
    )
    # Store provider specific data (like stripe intent ID)
    transaction_id = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=200, unique=True, default='')
    verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True, default='')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.status} - {self.reference}"


# Example of extension
class BankTransferDetail(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    reference = models.CharField(max_length=50) # Important for matching


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, related_name='wishlists', 
      on_delete=models.CASCADE, default=''
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'products')  # prevents duplicates

    def __str__(self):
        return f"{self.user} -> {self.products}"

    def get_total_price(self):
        return self.products


