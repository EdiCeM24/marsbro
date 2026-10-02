from django.contrib import admin
from .models import (
    Category,
    Products,
    Review,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Payment,
    Wishlist,
    SubCategory,
    ProductImage,
    ProductVariant,
    PurchaseHistories,
    Color,
    Size
)

# removed self as 2nd parameter:
def total_price(obj):
    return obj.get_total()

LIST_PER_PAGE = 20

# ----------------------------
# CATEGORY ADMIN
# ----------------------------
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'product__name', 'user__username')
    # list_filter = ('parent', 'name')

admin.site.register(Category, CategoryAdmin)

# ----------------------------
# SUBCATEGORY ADMIN
# ----------------------------
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(SubCategory, SubcategoryAdmin)


# ----------------------------
# PRODUCT IMAGE ADMIN
# ----------------------------
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_variant', 'image', 'position', 'is_primary')

admin.site.register(ProductImage, ProductImageAdmin)


# ----------------------------
# PRODUCT VARIANT ADMIN
# ----------------------------
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'sku', 'price', 'stock')

admin.site.register(ProductVariant, ProductVariantAdmin)


# ----------------------------
# PURCHASE HISTORIES ADMIN
# ----------------------------
class PurchaseHistoriesAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'total_price')

admin.site.register(PurchaseHistories, PurchaseHistoriesAdmin)


# ----------------------------
# SUBCATEGORY ADMIN
# ----------------------------
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code')


# ----------------------------
# SUBCATEGORY ADMIN
# ----------------------------
admin.site.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    

# ----------------------------
# PRODUCT ADMIN
# ----------------------------
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'category', 'subcategory', 'price', 'brand', 'stock', 'desc', 'available', )
    list_filter = ('available', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'available')

admin.site.register(Products, ProductsAdmin)


# ----------------------------
# REVIEW ADMIN
# ----------------------------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating')
    list_filter = ('rating',)
    search_fields = ('product__name', 'user__username')


# ----------------------------
# CART ITEM INLINE
# ----------------------------
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


# ----------------------------
# CART ADMIN
# ----------------------------
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', )
    inlines = [CartItemInline]


# ----------------------------
# ORDER ITEM INLINE
# ----------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# ----------------------------
# ORDER ADMIN
# ----------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username',)
    inlines = [OrderItemInline]


# ----------------------------
# PAYMENT ADMIN
# ----------------------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'transaction_id', 
        'verified',  'reference', 'payment_method', 
        'email'
    )
    list_filter = ('status',)
    search_fields = ('transaction_id', 'user__username')
    readonly_fields = ('transaction_id',)


# ----------------------------
# WISHLIST ADMIN
# ----------------------------
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'products')
    search_fields = ('user__username', 'product__name')




# admin.py
# from django.contrib import admin
# from .models import Order, Payment

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('user', 'reference', 'total_amount', 'status', 'created_at')
#     list_filter = ('status',)

# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'reference', 'amount', 'verified', 'created_at')


