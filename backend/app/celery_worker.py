from celery import Celery
import os

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
        backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
    )
    celery.conf.update(app.config)
    return celery
