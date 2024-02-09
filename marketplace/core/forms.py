# usato per creare utenti e validare
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User # db model

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
    }))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')    # pwd, ripeti pwd

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'w-full py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'w-full py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
    }))