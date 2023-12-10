from django.shortcuts import render

from item.models import Category, Item

# home page
# request: info della richiesta (browser, get/post, ..), da mettere in ogni view
def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]  # solo quelli in vendita, max 6
    categories = Category.objects.all()    # tutte le categorie
    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })   # ritorna un template


def contact(request):
    return render(request, 'core/contact.html')