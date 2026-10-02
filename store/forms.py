import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import CustomUser, Contact
from django.core.validators import EmailValidator
# from .models import User
from .models import Subscriber


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'username', 
            'profile_picture', 'email', 
            'password1', 'password2'
        ]

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if not profile_picture:
            self.add_error('profile_picture', 'Please upload profile image.')
            raise forms.ValidationError('Please upload a prfile image.')
        if profile_picture.size > 3 * 1024 * 1024:  # 3MB limit
            self.add_error('profile_picture', 'Profile image size must be at least 3MB.')  
            raise forms.ValidationError('Profile picture size should not exceed 3MB.') 
        return profile_picture

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            self.add_error('email', 'Email already registered. Please, try some other email.')
            raise forms.ValidationError('Email already registered. Please, try some other email.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if len(password1) < 8:
            self.add_error('password1', 'Password must be at least 8 characters long.')
            raise forms.ValidationError('password must be at least 8 characters.')
        if not re.search(r'[A-Z]', password1):
            self.add_error('password1', 'password must contain at least one uppercase letter.')
            raise forms.ValidationError('password must contain at least one uppercase letter.')

        if not re.search(r'[a-z]', password1):
            self.add_error('password1', 'password must contain at least one lowercase letter.')
            raise forms.ValidationError('password must contain at least one lowercase letter.')

        if not re.search(r'[0-9]', password1):
            self.add_error('password1', 'password must contain at least one number.')
            raise forms.ValidationError('password must contain at least one number.')

        if password1 and password2 and password1 != password2: 
            self.add_error('password1 and password2', 'passwords do not match.')
            raise forms.ValidationError('Passwords do not match.')
        return password1


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
      label='Email Address', widget=forms.TextInput(attrs={'autofocus': True})
    )
    #username = forms.EmailField(label='username')
    # password = forms.PasswordInput(
    # label='password', widget=forms.TextInput(attrs={'autofocus': True})
    #)


class ContactForm(forms.Form):
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


class PasswordResetRequestForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254)

    def clean_email(self):
        email = self.cleaned_data['email'] # check this clean_data
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email not found')
        return email
    

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('email', )