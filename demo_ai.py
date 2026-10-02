# how can we write code to implement category, 
# color, size, front, back and sides in django 
# project using CustomUser as user authentication?

# For a production-level Django e-commerce project, 
# you should not store colors, sizes, front, back, 
# and side images directly inside the Product model. 
# Instead, normalize the database.

# A good architecture looks like this:

# accounts/
#     models.py        # CustomUser

# categories/
#     models.py        # Category, SubCategory

# products/
#     models.py        # Product
                     # ProductVariant
                     # Color
                     # Size
                     # ProductImage

# media/
# Step 1: Custom User
# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="users/", blank=True, null=True)

    def __str__(self):
        return self.username

settings.py

AUTH_USER_MODEL = "accounts.CustomUser"
# Step 2: Category Model
# categories/models.py

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
# Step 3: SubCategory
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

# Example

# Fashion
#     Shoes
#     Shirts
#     Bags

# Electronics
#     Phones
#     Laptops
# Step 4: Color Model

# Never store color names repeatedly.

# products/models.py

class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7)

    def __str__(self):
        return self.name

# Example

# Black
# White
# Blue
# Red
# Green
# Step 5: Size Model
class Size(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

# Example

# XS
# S
# M
# L
# XL
42
43
44
45
# Step 6: Product Model
from django.conf import settings

class Product(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )

    category = models.ForeignKey(
        Category,
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

    name = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    description = models.TextField()

    brand = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Notice:

# No colors

# No sizes

# No images

# Those belong to variants.

# Step 7: Product Variant

# This is where production systems shine.

class ProductVariant(models.Model):

    product = models.ForeignKey(
        Product,
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

    sku = models.CharField(max_length=50, unique=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.color.name} - {self.size.name}"

# Example

# Nike Shoe

# Variant 1

# Color: Black
# Size: 42
# Price: 100
# Stock: 10

# Variant 2

# Color: White
# Size: 43
# Price: 120
# Stock: 5

# Variant 3

# Color: Blue
# Size: 44
# Price: 110
# Stock: 15
# Step 8: Product Images

# Instead of

# front_image
# back_image
# side_image
# left_image

# create one table.

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

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="products/")

    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES
    )

    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.variant} - {self.position}"

# Now one variant can have

# Front

# Back

# Left

# Right

# Top

# Bottom

# Packaging

# 360°

# Anything

# No need to add new database columns.

# Step 9: Database Relationship
# CustomUser
#       │
#       │
#       ▼
#  Product
#       │
#       ├──────────────► Category
#       │
#       ├──────────────► SubCategory
#       │
#       ▼
#  ProductVariant
#       │
#       ├────────► Color
#       │
#       ├────────► Size
#       │
#       ▼
#  ProductImage
# Example Data
# User
# -----
# John

# Category
# ---------
# Fashion

# SubCategory
# -----------
# Shoes

# Product
# -------
# Nike Air Max

# Variant
# -------
# Black
# 42
# $120

# Variant
# -------
# White
# 43
# $125

# Variant
# -------
# Blue
# 44
# $130

# Images

# Front

# Back

# Left

# Right
# Fetching Products with Variants
products = Product.objects.select_related(
    "category",
    "subcategory",
    "owner"
).prefetch_related(
    "variants__color",
    "variants__size",
    "variants__images",
)

# In a Django template:

# {% for product in products %}
#     <h2>{{ product.name }}</h2>

#     {% for variant in product.variants.all %}
#         <p>{{ variant.color.name }}</p>
#         <p>{{ variant.size.name }}</p>
#         <p>${{ variant.price }}</p>

#         {% for image in variant.images.all %}
#             <img src="{{ image.image.url }}" width="150">
#         {% endfor %}
#     {% endfor %}
# {% endfor %}
# Recommended production enhancements

# For a scalable marketplace or e-commerce application, consider adding these models and relationships:

# Brand
# Tag (many-to-many with Product)
# Attribute and AttributeValue (e.g., Material, Gender, Storage, RAM)
# ProductReview
# Wishlist
# Cart and CartItem
# Order and OrderItem
# Inventory with stock movement history
# ProductVideo
# ProductSpecification
# ProductSEO (meta title, description, keywords)
# Soft deletion (is_deleted) and audit fields (created_by, updated_by)
# Automatic slug generation and unique SKU generation
# Image optimization and thumbnail generation
# Database indexes on frequently queried fields (slug, category, brand, is_active, price)

# This design follows the same normalized approach used by large e-commerce platforms: the Product stores the core information, ProductVariant stores purchasable combinations (color, size, SKU, stock, price), and ProductImage stores any number of images for each variant, tagged by position (front, back, left, right, etc.). It scales well as your catalog grows and avoids duplicated data.