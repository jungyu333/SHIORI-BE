import asyncio

from celery.utils.log import get_task_logger
from shiori.app.celery import celery_app
from shiori.app.container import Container

task_logger = get_task_logger(__name__)


@celery_app.task(name="summary_task", bind=True, max_retries=3)
def summary_task(self, payload: dict):

    container = Container()

    diary_service = container.diary_service()

    user_id = payload["user_id"]
    start = payload["start"]
    end = payload["end"]
    week_inputs = payload["week_inputs"]
    diary_meta_ids = payload["diary_meta_ids"]
    dates = payload["dates"]

    try:
        result = asyncio.run(
            diary_service.summarize_diary(
                user_id=user_id,
                start=start,
                end=end,
                week_inputs=week_inputs,
                diary_meta_ids=diary_meta_ids,
                dates=dates,
            )
        )

        return {"status": "ok", "result": result}
    except Exception as e:

        if isinstance(e, (TimeoutError, ConnectionError)):
            raise self.retry(exc=e, countdown=15)

        raise e
