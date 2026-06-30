from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.contrib.auth.mixins import PermissionRequiredMixin # This is the 2nd problem
from django.conf import settings
from .validators import validations
from django.utils import timezone
from datetime import timedelta

User = settings.AUTH_USER_MODEL


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
        ('user', 'User'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)

    def is_admin(self):
        return self.role == 'admin'

    def is_vendor(self):
        return self.role == 'vendor'

class Product(models.Model):
    topic = models.CharField(max_length=30)
    text = models.CharField(verbose_name='text', max_length=100)


class Blog(models.Model):
    topic = models.CharField(max_length=60)
    details = models.TextField(verbose_name='message', max_length=1000)
    image = models.ImageField(upload_to='uploads', blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=120, unique=True, blank=False, null=False)
    phone_number = models.PositiveIntegerField(blank=False, null=False)
    website = models.URLField(unique=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=120, blank=False, null=False)
    message = models.TextField(max_length=1000, blank=False, null=False)


class SliderImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='slider_images/')
    text = models.CharField(max_length=200, blank=True, null=True)

 
class HomeScreen(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='upload', validators=[validations], blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=True)


class BlacklistedUser(models.Model):
  email = models.EmailField(unique=True)
  blacklisted_at = models.DateTimeField(auto_now_add=True)
  expires_at = models.DateTimeField()

  def __str__(self):
    return self.email
  
  def save(self, *args, **kwargs):
    self.expires_at = timezone.now() + timedelta(days=30)
    super().save(*args, **kwargs)


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Add 'username' here
    profile_picture = models.ImageField(
        upload_to='images', validators=[validations],
        blank=True, null=True
    )

    def __str__(self):
        return self.email
    

class CustomUserManager(BaseUserManager):
  def create_user(self, email, password=None):
    if not email:
      raise ValueError('Users must have an email address')
    
    user = self.model(
      email=self.normalize_email(email),
    )

    user.set_password(password)
    user.save(using=self._db)

    return user
  
  def create_superuser(self, email, password=None):
    user = self.create_user(
      email,
      password=password,
    )
    user.is_admin = True
    user.save(using=self._db)
    return user
  
class User(AbstractBaseUser, PermissionRequiredMixin):
  email = models.EmailField(unique=True)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=True)
  date_joined = models.DateTimeField(default=timezone.now)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.email

  def has_perm(self, perm, obj=None):
    return True

  def has_module_perms(self, app_label):
    return True  
  
  @property
  def is_staff(self):
    return self.is_admin

