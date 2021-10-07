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
    username = forms.EmailField(
        max_length=30, required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter the Email'}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password', 'class': 'password'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password', 'class': 'password'
            }
        )
    )
        
    # reCaptcha token
    token = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'password1', 'password2'
        )


class AuthForm(AuthenticationForm):     # user auth
    username = forms.EmailField(
        max_length=50, required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'Email'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'password'}
        )
    )

    class Meta:
        model = User
        fields = (
            'username', 'password',
        )


# basic model form for the user profile that extends Django user model
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(
        max_length=100, required=True, widget=forms.HiddenInput())  # hiddeninput will be hidden on the html file
    town = forms.CharField(
        max_length=100, required=True, widget=forms.HiddenInput())
    county = forms.CharField(
        max_length=100, required=True, widget=forms.HiddenInput())
    post_code = forms.CharField(
        max_length=40, required=True, widget=forms.HiddenInput())
    country = forms.CharField(
        max_length=100, required=True, widget=forms.HiddenInput())
    longitude = forms.CharField(
        max_length=40, required=True, widget=forms.HiddenInput())
    latitude = forms.CharField(
        max_length=50, required=True, widget=forms.HiddenInput())

    class Meta:
        model = UserProfile
        fields = (
            'address', 'town', 'county', 'post_code', 'country', 'longitude', 'latitude'
        )
