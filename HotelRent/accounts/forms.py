from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, EmailValidator


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=32,
                               validators=[
                                   RegexValidator(regex=r'^[a-zA-Z]{1}[a-zA-Z0-9_\-]*',
                                                  message='Username must start with letters and contain only letters, '
                                                          'numbers, hyphens, or the underscore character when creating '
                                                          'a new user'),
                                   MinLengthValidator(3, message='Username must contain at least 3 symbols'),
                                   MaxLengthValidator(32, message='Username must be less or equal to 32 symbols')
                               ],
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(max_length=128,
                             validators=[EmailValidator],
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(max_length=32,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=32,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Repeat Password'}))
    terms_of_service = forms.BooleanField(required=True, disabled=False,
                                          widget=forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                                            'id': 'flexSwitchCheckDefault'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'terms_of_service']
