import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitly.settings')

app = Celery('bitly')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# settings.py (Celery Configuration)
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'