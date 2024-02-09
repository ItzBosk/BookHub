
"""This module contains the views for the marketplace app."""

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from item.models import Genre, Item
from .forms import SignupForm


def index(request):
    """View for the index page which displays genres and items."""
    items = Item.objects.filter(is_sold=False)[0:6]  # Uncomment when 'item.models' is accessible
    genres = Genre.objects.all()  # Uncomment when 'item.models' is accessible

    return render(request, 'core/index.html', {
        'genres': genres,
        'items': items,
    })

def contact(request):
    """View for the contact page."""
    return render(request, 'core/contact.html')

def signup(request):
    """View for the signup page where users can create an account."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})


def signout(request):
    """View to sign out the user."""
    logout(request)
    return redirect('core:index')


# Additional newline at the end of the file
