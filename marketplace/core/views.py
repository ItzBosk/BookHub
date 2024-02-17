from django.shortcuts import render, redirect
from django.contrib.auth import logout
from item.models import Genre, Item
from .forms import SignupForm


# home page
# request: info della richiesta (browser, GET/POST, ..), da mettere in ogni view
def index(request):
    items = Item.objects.filter(is_sold=False)[0:10]  # solo quelli in vendita, max 10
    genres = Genre.objects.all()  # tutti i generi

    return render(request, 'core/index.html', {
        'genres': genres,
        'items': items,
    })  # ritorna il template


def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':    # allora vuol dire che ho compilato la form
        form = SignupForm(request.POST)
        if form.is_valid():     # se ho compilato correttamente, salvo i dati e creo utente nel db
            form.save()
            return redirect('/login/')  # dopo aver salvato i dati faccio redirect a login
    else:   # se non è una post, faccio vuoto
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})

def signout(request):
    logout(request)  # Chiude la sessione dell'utente
    return redirect('core:index')  # Reindirizza alla home page