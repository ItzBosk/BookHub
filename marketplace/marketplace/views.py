from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import QueryForm
from .models import UserQuery

# lista ricerche
@login_required
def past_researches(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            # Create a new UserQuery object and save it
            query = UserQuery.objects.create(user=request.user, parameters=form.cleaned_data)
            query.save()

            # TODO: Redirect to query results page
            return redirect('dashboard')
    else:
        form = QueryForm()
    return render(request, 'marketplace/researches_list.html', {'form': form})

# lista libri che soddisfano una ricerca
@login_required
def query_results(request, query_id):
    user_query = UserQuery.objects.get(id=query_id, user=request.user)
    results = user_query.results.all()

    return render(request, 'query_results.html', {'results': results})

@login_required
def new_research(request):
    if request.method == 'POST':
        form = QueryForm(request.POST, request.FILES)     # salvo dati e file caricati
        if form.is_valid():
            query = form.save(commit=False)  # non salvo subito nel db perché non saprei chi ha creato il prodotto
            query.created_by = request.user
            query.save()
            return redirect('query_results', pk=query.id)  # research salvata, redirect a risultati query
    else:   # se fosse una GET request
        form = QueryForm()

    return render(request, 'marketplace/form.html', {
        'form': form,
        'title': 'New research',
    })