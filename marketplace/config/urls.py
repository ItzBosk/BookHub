from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'config'

urlpatterns = [
    path('', include('core.urls')),
    path('items/', include('item.urls')),   # collega ogni url che inizia con item al file item/urls.py
    path('dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls),
    path('researches_list/', views.past_researches, name='past_researches'),
    path('form/', views.new, name='new'),
    path('query_results/<int:query_id>/', views.results, name='results'),
    path('delete/<int:query_id>/', views.delete, name='delete'),
    path('edit/<int:query_id>/', views.edit, name='edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # gestione immagini
