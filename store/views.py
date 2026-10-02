from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import *
import re
from dotenv import load_dotenv
import os
from django.core.paginator import Paginator
import mailtrap as mt
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, LoginForm, ContactForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .validators import validations
from django.conf import settings
# PASSWORD RESET SECTION
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
import requests
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse
from .forms import PasswordResetRequestForm, Subscriber
from .models import CustomUser
from django.db.models import Q
# from .forms import SubscribeForm, Subscriber


load_dotenv()

@login_required(login_url='login')
def home (request):
    products = Product.objects.all()

    total_count = Product.objects.count()
    paginator = Paginator(products, 25)
    page = request.GET.get('page', 1)
    product = paginator.get_page(page)

    sort_by = request.GET.get('sort_by')
    if sort_by == 'name_asc':
        products = Product.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')

    return render(request, 'home/index.html', {
      'products': products,
      'total_count': total_count,
      'product': product,
    })

@login_required(login_url='login')
def blogs(request):
    blog = Blog.objects.all()
    return render(request, 'home/blogs.html', {
      'blog': blog
    })

@login_required(login_url='login')
def about(request):

    return render(request, 'context/about.html', {
  
    })


# def search_products(request):
#     query = request.GET.get('q')
#     if query:
#         products = Product.objects.filter(Q(topic__icontains=query) | Q(text__icontains=query))
#     else:
#         products = Product.objects.all()
#     return render(request, 'context/search_products.html', {
#         'products': products,
#     })    

# SUBSCRIPTION SECTION
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('subscribe')

        if email:
            if Subscriber.objects.filter(email=email).exists():
                messages.error(request, 'You are already subscribed to our newsletter.')
            else:
                Subscriber.objects.create(email=email)
                messages.success(request, 'You have been subscribed to our newsletter.')
            return redirect('home')
        else:
            messages.error(request, 'Please enter a valid email address.')
            return redirect('home')    
    return render(request, 'includes/footer.html')                

# THIS IS FROM FORMS.PY FORMAT OF SUBSCRIPTION:
# def subscribe(request):
#     if request.method == 'POST':
#         form = SubscribeForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             if Subscriber.objects.filter(email=email).exists():
#                 messages.error(request, 'You are already subscribed to our newsletter.')
#             else:
#                 form.save()
#                 messages.success(request, 'You have been subscribed to our newsletter.')
#             return redirect('home')
#     else:
#         form = SubscribeForm()
#     return render(request, 'includes/footer.html', {'form': form})                


def send_newsletter(request):
    subject = 'Your newsletter subject' # To check and add the need here.
    message = 'Your newsletter message' # To check and add the need here.
    from_email = settings.DEFAULT_FROM_EMAIL
    recipients = [subscriber.email for subscriber in Subscriber.objects.all()]
    send_mail(subject, message, from_email, recipients)
    return redirect('home')


API_TOKEN = str(os.getenv('MAILTRAP_API_TOKEN'))
#"<YOUR_API_TOKEN>"
@login_required(login_url='login')
def contact(request):
    client = mt.MailtrapClient(token=API_TOKEN)

    if request.method == 'POST':
        form = ContactForm(request.POST)
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
      
        try:
            # Send an email by using send_mail
            mail = mt.Mail(
                email,  # From email
                [settings.ADMIN_EMAIL],  # To email
                                
                sender=mt.Address(email="sales@example.com", name="My App Sales"),
                to=[mt.Address(email="recipient@example.com")],
                subject= f'From {name}, Subject: {subject} Welcome to our app!',
                text="This is a plain text email sent via the Mailtrap API SDK.",
                category="onboarding" # Optional: for analytics
                  f'Message: {message}\nContact Phone: {phone_number}',
                  ail_silently=False,
            )      
            client.send(mail)
            # Process the form data
            form.save()
            messages.success(request, 'Your message has been sent successfully. ✅')
            print("Email sent successfully to production!")
            return redirect('contact')
        except Exception as e:
            print(f"Failed to send email: {e}")
    else:
        form = ContactForm()
        messages.error(request, 'Invalid form submission')

    return render(request, 'context/contact.html', {
      'form': form,
    })
        




@login_required(login_url='login')
def screens(request):
  vids = HomeScreen.objects.all()
  #video size to upload will be restricted


  # Upload of video must abide by some certain rules
  return render(request, 'home/screens.html', {
    'vids': vids,
  })


def registerView(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form .is_valid():
            messages.success(request, 'Account created successfully ✅')
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

            user = authenticate(request, username=email_as_username, password=password)

            if user is not None:
                messages.success(request, f"You are now logged in as {user.username} ✅")
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
                form = LoginForm()

    return render(request, 'auth/login.html', {
      'form': form,
    })


def password_reset_view(request):
  if request.method == 'POST':
    form = PasswordResetRequestForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        user = CustomUser.objects.get(email=email)
        token = default_token_generator.make_token(user)
        reset_url = request.build_absolute_uri(reverse('password_reset_confirm', args=[user.pk, token]))
        send_mail(
            'Password Reset',
            f'Click the link to reset your password: {reset_url}',
            'xemars24@gmail.com',
            [email],
            fail_silently=False,
        )
        return HttpResponseRedirect(reverse('password_reset_done_view'))
  else:
    form = PasswordResetRequestForm()  
    return render(request, 'auth/password_reset.html')


def password_reset_done_view(request):
    return render(request, 'auth/password_reset_done.html')


def password_reset_confirm_view(request, pk, token):
  user = CustomUser.objects.get(pk=pk)
  if default_token_generator.check_token(user, token):
      if request.method == 'POST':
          password = request.POST['password']
          user.set_password(password)
          user.save()
          return HttpResponseRedirect(reverse('password_reset_complete_view'))
      return render(request, 'auth/password_reset_confirm.html')
  return HttpResponseRedirect(reverse('password_reset_invalid'))


def password_reset_complete_view(request):
  return render(request, 'auth/password_reset_complete.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You are logged out successsfully! ✅')
    return redirect('login')



