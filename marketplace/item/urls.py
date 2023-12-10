from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    # si aspetta un integer come private key, e sarà lo stesso espresso nella richiesta in item/view.py
    path('<int:pk>/', views.detail, name='detail'),
]