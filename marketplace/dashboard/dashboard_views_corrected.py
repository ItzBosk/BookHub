"""Module for dashboard views in the marketplace application."""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from item.models import Item


"""View function for the dashboard index page."""
"""Display the dashboard index page."""
@login_required
def index(request):
    """Display the dashboard index page."""
    """Display the dashboard index page."""
    items = Item.objects.filter(created_by=request.user)

    return render(request, 'dashboard/index.html', {
        'items': items,
    })
