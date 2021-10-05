from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms


class UserForm(UserCreationForm):   # user creation
    first_name = forms.CharField(
        max_length=40, required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter your First Name'}
        )
    )

    last_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter your Second Name'}
        )
    )
    email = forms.CharField(
        max_length=30, required=True,
        widget=forms.EmailField(
            attrs={'placeholder': 'Enter the Email'}
        )
    )
    password1 = forms.TextInput(
        attrs={'placeholder': 'Password', 'class': 'password'}
    )
    password2 = forms.TextInput(
        attrs={'placeholder': 'Confirm Password', 'class': 'password'}
    )
    
    token = forms.CharField(
        widget=forms.HiddenInput()
    )
    
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2'
        )
        

class AuthForm(AuthenticationForm):     # user auth
    username = forms.EmailField(
        max_length=50, required=True,
        widget = forms.TextInput(
            attrs={'placeholder': 'Email'}
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'password'}
        )
    )
    
    class Meta:
        model = User
        fields = (
            'username', 'password',
        )