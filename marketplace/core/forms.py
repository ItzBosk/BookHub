#usato per creare utenti e validare
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User #db model

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')