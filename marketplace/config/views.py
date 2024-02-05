from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import NewQueryForm, EditQueryForm
from .models import UserQuery, Item

# lista ricerche
@login_required
def past_researches(request):
    # Recuperare le ricerche passate dell'utente loggato
    past_queries = UserQuery.objects.filter(user=request.user)
    return render(request, 'config/researches_list.html', {'past_queries': past_queries})

# lista libri che soddisfano una ricerca
@login_required
def results(request, query_id):
    user_query = UserQuery.objects.get(id=query_id, user=request.user)

    # costruzione filtro
    query_filter = Q()
    if user_query.title:
        query_filter &= Q(title__icontains=user_query.title)
    if user_query.author:
        query_filter &= Q(author__icontains=user_query.author)
    if user_query.description:
        query_filter &= Q(description__icontains=user_query.description)

    # se il campo è una ForeignKey
    if user_query.genre:
        query_filter &= Q(genre__name__icontains=user_query.genre.name)
    if user_query.format:
        query_filter &= Q(format__name__icontains=user_query.format.name)
    if user_query.language:
        query_filter &= Q(language__name__icontains=user_query.language.name)

    # range di prezzo
    if user_query.min_price is not None:
        query_filter &= Q(price__gte=user_query.min_price)
    if user_query.max_price is not None:
        query_filter &= Q(price__lte=user_query.max_price)

    items = Item.objects.filter(query_filter)
    return render(request, 'config/query_results.html', {'results': items})

@login_required
def new(request):
    # se la form è stata inviata con dei dati al suo interno    
    if request.method == 'POST':
        form = NewQueryForm(request.POST)     # salvo dati
        if form.is_valid():
            query = form.save(commit=False)  # non salvo subito nel db perché non saprei chi ha creato il prodotto
            query.user = request.user
            query.save()
            return redirect(results, query_id=query.id)  # research salvata, redirect a risultati query
    else:   # se fosse una GET request
        form = NewQueryForm()

    return render(request, 'config/form.html', {
        'form': form,
        'title': 'New research',
    })

@login_required
def edit(request, query_id):
    query = get_object_or_404(UserQuery, pk=query_id, user=request.user)
    if request.method == 'POST':
        form = EditQueryForm(request.POST, instance=query)
        if form.is_valid():
            form.save()
            return redirect(results, query_id=query.id)
    else:  # se fosse una GET request
        form = EditQueryForm(instance=query)

    return render(request, 'config/form.html', {
        'form': form,
        'title': 'New research',
    })

@login_required
def delete(request, query_id):
    query = get_object_or_404(UserQuery, pk=query_id, user=request.user)
    query.delete()
    return redirect(past_researches)