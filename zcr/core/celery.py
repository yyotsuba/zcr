from celery import Celery

from zcr.config.settings import settings

app = Celery('zcr')

app.config_from_object(settings.CELERY_CONF)
