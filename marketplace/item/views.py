from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Item
from .forms import NewItemForm

# ricerca elemento in base a richiesta e primary key
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)   # se non presente da errore
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]


    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

# nuovo prodotto solo se ho fatto il login, altrimenti redirect al log in
@login_required
def new(request):
    form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })