from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Contact
import re
from django.core.validators import EmailValidator


class SignupForm(UserCreationForm):
  class Meta:
    model = CustomUser
    fields = ['first_name', 'last_name', 'username', 'profile_picture', 'email', 'password1', 'password2']
  
  def clean_email(self):
    email = self.cleaned_data.get('email')
    if CustomUser.objects.filter(email=email).exists():
      raise forms.ValidationError('Email already registered. Please, try some other email.')
    return email
  
  def clean_password1(self):
    password = self.cleaned_data.get('password1')
    if len(password) < 8:
      raise forms.ValidationError('password must be at least 8 characters.')
    if not re.search(r'[A-Z]', password):
      raise forms.ValidationError('password must contain at least one uppercase letter.')
    
    if not re.search(r'[a-z]', password):
      raise forms.ValidationError('password must contain at least one lowercase letter.')
    
    if not re.search(r'[0-9]', password):
      raise forms.ValidationError('password must contain at least one number.')
    return password
  

class LoginForm(AuthenticationForm):
  username = forms.EmailField(label='Email Address', widget=forms.TextInput(attrs={'autofocus': True}))
  #username = forms.EmailField(label='username')
  # password = forms.EmailField(label='password')


class Contact(forms.Form):
  class Meta:
    models = Contact 
    name = forms.CharField(max_length=100)
    email = forms.CharField(validators=[EmailValidator()])
    website = forms.URLField()
    company_name = forms.CharField(max_length=200)
    phone_number = forms.CharField(max_length=15)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    fields = ['name', 'email', 'company_name', 'website', 'message', 'subject', 'phone_number']
