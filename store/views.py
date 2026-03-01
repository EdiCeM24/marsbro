from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate, logout
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
from .validators import validations
import requests
from django.contrib.auth.models import User, auth


def home (request):
  products = Product.objects.all()
  total_count = Product.objects.count()
  return render(request, 'home/index.html', {
    'products': products,
    'total_count': total_count,
  })


def blogs(request):
  blog = Blog.objects.all()
  return render(request, 'home/blogs.html', {
    'blog': blog
  })


def about(request):
  
  return render(request, 'context/about.html', {
  
  })


def contact(request):
  if request.method == 'POST':
    form = Contact(request.POST)
    if form.is_valid():
      name = request.POST.get('name')
      email = request.POST.get('email')
      company_name = request.POST.get('company_name')
      website = request.POST.get('website')
      message = request.POST.get('message')
      subject = request.POST.get('subject')
      phone_number = request.POST.get('phone_number')

      if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        messages.error(request, 'Invalid email address')
        return redirect('contact')
      if name == '' or email == '' or company_name == '' or website == '' or message == '' or subject == '' or phone_number == '':
        messages.error(request, 'Please fill all fields')
        return redirect('contact')
    
      # Send an email
      send_mail(
        f'From {name}, Subject: {subject}',
        f'Message: {message}\nContact Phone: {phone_number}',
        email,  # From email
        [settings.ADMIN_EMAIL],  # To email
        fail_silently=False,
      )
      # Process the form data
      form.save()
      messages.success(request, 'Your message has been sent successfully.')
      return redirect('contact')
  else:
    form = Contact()
    messages.error(request, 'Invalid form submission')
  return render(request, 'context/contact.html', {
    'form': form,
  })





def screens(request):
  vids = HomeScreen.objects.all()
  #video size to upload will be restricted


  # Upload of video must abide by some certain rules
  return render(request, 'home/screens.html', {
    'vids': vids,
  })


def registerView(request):
  if request.method == 'POST':
    form = SignupForm(request.POST, request.FILES)
    if form .is_valid():
      messages.success(request, 'Account created successfully')
      user = form.save()
      #login(request, user)
      login(request, user, backend='django.contrib.auth.backends.ModelBackend') 
      return redirect('login')
  else:
    messages.error(request, "Invalid form submission")
    form = SignupForm()

  return render(request, 'auth/register.html', {
    'form': form,
  })


def loginView(request):
  form = LoginForm()
  if request.method == 'POST':
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
      email_as_username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')

      user = authenticate(request, email=email_as_username, password=password)

      if user is not None:
        messages.success(request, f"You are now logged in as {user.username}")
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend') 
        return redirect('home')
  else:
    messages.error(request, "Invalid username or password.")
    form = LoginForm()
  return render(request, 'auth/login.html', {
    'form': form,
  })


def passwordResetView(request):
  # Here we write view
  return render(request, 'auth/password_reset.html')


def passwordResetDoneView(request):
  return render(request, 'auth/password_reset_done.html')


def passwordResetConfirmView(request):
  # we write a view
  return render(request, 'auth/password_reset_confirm.html')


def passwordResetCompleteView(request):
  return render(request, 'auth/password_reset_complete.html')


def logout_view(request):
  auth.logout(request)
  messages.success(request, 'You are logged out successsfully!')
  return redirect('login')

