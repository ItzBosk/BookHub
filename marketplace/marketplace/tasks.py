from celery import shared_task
from .models import UserQuery, Item
from django.db.models import Q

@shared_task
def run_user_queries():
    for user_query in UserQuery.objects.all():
        query = Q()
        for param, value in user_query.parameters.items():
            query &= Q(**{param: value})
        new_results = Item.objects.filter(query)
        existing_results = user_query.results.all()

        # Check for new items not in existing results
        new_items = new_results.exclude(id__in=existing_results)

        # Check if new results are found compared to the previous run
        if new_results.exists():
            print(f"New items found for User {user_query.user.username}'s search query!")
            user_query.results.add(*new_items)  # Add new items to the query's results
