from celery import shared_task
from .models import UserQuery, Item
from django.db.models import Q

@shared_task
def run_user_queries():
    for user_query in UserQuery.objects.all():

        # costruzione filtro
        query_filter = Q()

        # campi liberi
        if user_query.title:
            query_filter &= Q(title__icontains=user_query.title)
        if user_query.author:
            query_filter &= Q(author__icontains=user_query.author)
        if user_query.description:
            query_filter &= Q(description__icontains=user_query.description)

        # campi con dei preset
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

        new_results = Item.objects.filter(query_filter)
        existing_results = user_query.results.all()

        # trova nuovi prodotti escludendo gli ID di quelli che erano già presenti
        new_items = new_results.exclude(id__in=[item.id for item in existing_results])

        # controlla se ci sono dei nuovi prodotti rispetto all'esecuzione precedente
        if new_items.exists():
            print(f"New items found for user {user_query.user.username}'s search query!")
            user_query.results.add(*new_items)  # se ci sono li aggiunge ai risultati della ricerca
