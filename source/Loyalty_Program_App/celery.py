import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Loyalty_Program_App.settings')
app = Celery('Loyalty_Program_App')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
