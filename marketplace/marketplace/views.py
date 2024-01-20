from django.shortcuts import render, redirect
from .forms import QueryForm
from .models import UserQuery

def query_view(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            # Create a new UserQuery object and save it
            query = UserQuery.objects.create(user=request.user, parameters=form.cleaned_data)
            query.save()
            # Redirect to the dashboard or query results page
            return redirect('dashboard')
    else:
        form = QueryForm()

    return render(request, 'query_form.html', {'form': form})

def query_results_view(request, query_id):
    user_query = UserQuery.objects.get(id=query_id, user=request.user)
    results = user_query.results.all()

    return render(request, 'query_results.html', {'results': results})