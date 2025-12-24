from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "intelligent_doc_service",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)

celery_app.conf.task_acks_late = True

celery_app.conf.task_default_queue = 'default'

# Define shared queue
celery_app.conf.task_queues = {
    'pdf_processing': {
        'exchange': 'pdf_exchange',
        'routing_key': 'pdf_processing',
    },
}

celery_app.autodiscover_tasks()

import app.tasks