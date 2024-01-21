from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

# from marketplace.core.views import index, contact

app_name = 'marketplace'

urlpatterns = [
    #path('', views.query_view, name='query_view'),
    path('', include('core.urls')),
    path('items/', include('item.urls')),   # collega ogni url che inizia con item al file item/urls.py
    # path('contact/', contact, name='contact'),
    path('dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls),
    path('researches_list/', views.past_researches, name='past_researches'),
    path('form/', views.new_research, name='new_research'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # gestione immagini
