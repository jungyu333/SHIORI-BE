from celery import Celery
from shiori.app.core import get_settings

config = get_settings()

celery_app = Celery(
    "shiori-worker",
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_BACKEND_URL,
)

celery_app.conf.task_routes = {
    "worker.tasks.summary_task": {"queue": "summary-queue"},
}

celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Seoul",
    enable_utc=True,
)
