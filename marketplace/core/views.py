from django.shortcuts import render

# home page
# request: info della richiesta (browser, get/post, ..), da mettere in ogni view
def index(request):
    return render(request, 'core/index.html')