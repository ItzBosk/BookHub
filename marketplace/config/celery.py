from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# imposta il modulo delle impostazioni Django predefinito per celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# namespace condiviso da tutti i worker
app.config_from_object('django.conf:settings', namespace='CELERY')

# cerca i task in tutte le app Django registrate
app.autodiscover_tasks()
