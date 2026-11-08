from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
import re

class RegisterForm(UserCreationForm):
    # Explicitly define fields for better control
    first_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[MinLengthValidator(2), MaxLengthValidator(30)],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter first name'
        })
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[MinLengthValidator(2), MaxLengthValidator(30)],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter last name'
        })
    )

    username = forms.CharField(
        max_length=20,
        min_length=4,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='Username can only contain letters, numbers, and underscores.'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username (4-20 chars)'
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )

    phone = forms.CharField(
        max_length=10,
        min_length=10,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^[6789]\d{9}$',
                message='Phone number must be 10 digits and start with 6,7,8, or 9.'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 10-digit mobile number (optional)'
        })
    )

    profile = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password (min 8 chars)'
        }),
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                message='Password must contain at least 1 uppercase, 1 lowercase, 1 number, and 1 special character.'
            )
        ]
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = Register
        fields = [
            'first_name', 'last_name', 'username', 'email', 'phone',
            'profile', 'password1', 'password2'
        ]
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'Email Address',
            'phone': 'Phone Number (Optional)',
            'profile': 'Profile Picture (Optional)',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Register.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Register.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please use another email.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^[6789]\d{9}$', phone):
            raise ValidationError("Phone number must be exactly 10 digits starting with 6,7,8, or 9.")
        return phone

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2

    def clean_profile(self):
        profile = self.cleaned_data.get('profile')
        if profile:
            if profile.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError("Profile image must be less than 5MB.")
        return profile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders for better UX
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter 10-digit mobile number (optional)'


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Places
        fields = [
            'name',
            'location',
            'description',
            'image',
            'category',
            'entry_fee',
            'rating',
            'opening_time',
            'closing_time',
            'best_season',
        ]

        labels = {
            'name': 'Place Name',
            'location': 'Location',
            'description': 'Description',
            'image': 'Place Image',
            'category': 'Category',
            'entry_fee': 'Entry Fee (₹)',
            'rating': 'Rating',
            'opening_time': 'Opening Time',
            'closing_time': 'Closing Time',
            'best_season': 'Best Season to Visit',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter place name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter location'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter description'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'entry_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter entry fee'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '5',
                'placeholder': 'Rating (0–5)'
            }),
            'opening_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'closing_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'best_season': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Eg: October – March'
            }),
        }
