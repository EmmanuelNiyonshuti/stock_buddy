from app import create_app
from app.services.notification_service import send_sms
from .celery_worker import make_celery

app = create_app()

celery = make_celery(app)

@celery.task
def send_sms_task(to, body):
    return send_sms(to, body)
