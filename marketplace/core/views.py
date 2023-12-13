from django.shortcuts import render, redirect
from item.models import Category, Item
from .forms import SignupForm

from .forms import SignupForm

# home page
# request: info della richiesta (browser, GET/POST, ..), da mettere in ogni view
def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]  # solo quelli in vendita, max 6
    categories = Category.objects.all()  # tutte le categorie

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })  # ritorna un template


def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST': #allora vuol dire che ho compilato la form
        form = SignupForm(request.POST)

        if form.is_valid(): #se ho compilato correttamente, salvo i dati
            form.save()
            return redirect('/login/') #dopo aver salvato i dati faccio redirect a login
    else: #se non e' una post, faccio vuoto
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})