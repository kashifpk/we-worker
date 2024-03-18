from celery import Celery

from .settings import get_settings
from .worker import run_worker  # noqa: F401

settings = get_settings()

celery_app = Celery("we-worker", broker=settings.broker_url)
celery_app.autodiscover_tasks()
celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    result_compression='bzip2',
    task_compression='bzip2',
    worker_prefetch_multiplier=settings.worker_prefetch_multiplier,
)
