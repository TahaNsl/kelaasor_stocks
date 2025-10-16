import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_exchange.settings')

app = Celery('stock_exchange')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-company-prices-every-24h': {
        'task': 'companies.tasks.update_company_prices',
        'schedule': crontab(hour=0, minute=0),
    },
}
