from django.db.models import Q      # permette tramite una query di cercare nelle descrizioni degli oggetti
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Item, Genre, Language
from .forms import NewItemForm, EditItemForm

# lista degli item non venduti
def items(request):
    query = request.GET.get('query', '')    # permette la ricerca dei vari item nella sidebar
    genre_id = request.GET.get('genre', 0)
    genres = Genre.objects.all()
    items = Item.objects.filter(is_sold=False)
    languages = Language.objects.all()
    language_id = request.GET.get('language', 0)

    # ricerca per genere, mostra solo libri di quel genere
    if genre_id:
        items = items.filter(genre_id=genre_id)

    # ricerca per lingua, mostra solo libri di quella lingua
    if language_id:
        items = items.filter(language_id=language_id)

    # filtro le query con titolo o descrizione oggetto
    if query:
        # Q permette di cercare in campi multipli
        items = items.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(author__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'genres': genres,
        'genre_id' : int(genre_id),
        'languages': languages,
        'language_id': int(language_id)
    })

# ricerca elemento in base a richiesta e primary key
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)   # se non presente da errore
    related_items = Item.objects.filter(genre=item.genre, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

# nuovo prodotto solo se ho fatto il login, altrimenti redirect al log in
@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)     # salvo dati e file caricati
        if form.is_valid():
            item = form.save(commit=False)  # non salvo subito nel db perché non saprei chi ha creato la search
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)  # salvataggio fatto, redirect a pagina prodotto
    else:   # se fosse una GET request
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def delete(request, pk):
    # # pk = id prodotto da elininare
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')    # redirect a index

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)     # salvo dati e file caricati
        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.id)  # salvataggio fatto, redirect a pagina prodotto
    else:   # se fosse una GET request
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })