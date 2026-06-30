from django.contrib import admin
from .models import Product, BlacklistedUser, Blog, Contact, SliderImage, HomeScreen, CustomUser, UserProfile


class ProductAdmin(admin.ModelAdmin):
    list_display = ('topic', 'text')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('topic', 'details', 'image')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number',
       'website', 'company_name', 'subject', 'message'
    )

class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'text')

class HomeScreenAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'avatar')


class BlacklistedUserAdmin(admin.ModelAdmin):
  list_display = ('email', 'blacklisted_at', 'expires_at')


admin.site.register(BlacklistedUser, BlacklistedUserAdmin)

admin.site.register(Product, ProductAdmin)

admin.site.register(Blog, BlogAdmin)

admin.site.register(Contact, ContactAdmin)

admin.site.register(SliderImage, SliderImageAdmin)

admin.site.register(HomeScreen, HomeScreenAdmin)

admin.site.register(CustomUser)

admin.site.register(UserProfile, UserProfileAdmin)

# /admin/socialaccount/socialapp/

