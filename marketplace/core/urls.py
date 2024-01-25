from os import path

from django.contrib.auth import views as auth_views     # così non va in conflitto con import views
from django.urls import path, include

from . import views
from .forms import LoginForm
from marketplace.views import *

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html' , authentication_form=LoginForm), name='login'),
    path('user_past_queries/', past_researches, name='past_researches'),
    path('results/', results, name='results'),
    path('delete/', delete, name='delete'),
    path('signout/', views.signout, name='signout'),
]