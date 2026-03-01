from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .validators import *


class Product(models.Model):
  topic = models.CharField(max_length=30)
  text = models.CharField(verbose_name='text', max_length=100)

  def __str__(self):
    return self.topic
  
class Blog(models.Model):
  topic = models.CharField(max_length=60)
  details = models.TextField(verbose_name='message', max_length=1000)
  image = models.ImageField(upload_to='uploads', blank=True, null=True)
  updated = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.topic
  
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
  image = models.ImageField(upload_to='slider_images/') # Images will be stored in media/slider_images/
  text = models.CharField(max_length=200, blank=True, null=True)

  def __str__(self):
    return self.title
  
class HomeScreen(models.Model):
  title = models.CharField(max_length=100)
  image = models.FileField(upload_to='upload', validators=[validations], blank=True, null=True)
  updated = models.DateTimeField(auto_now_add=True)

class CustomUser(AbstractUser):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  username = models.CharField(max_length=50, unique=True, blank=False, null=False)
  email = models.EmailField(unique=True, blank=False, null=False)
  profile_picture = models.ImageField(upload_to='images', blank=True, null=True)
 

 
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['first_name', 'last_name']

  def __str__(self):
    return self.email

