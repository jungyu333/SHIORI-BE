import asyncio

import requests
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
        reflection, emotion_results = asyncio.run(
            diary_service.summarize_diary(
                week_inputs=week_inputs,
                diary_meta_ids=diary_meta_ids,
                dates=dates,
            )
        )
        response = requests.post(
            "http://host.docker.internal:8080/api/internal/summarize/result",
            json={
                "user_id": user_id,
                "start": start,
                "end": end,
                "reflection": reflection,
                "emotion_results": [
                    emotion_result.model_dump() for emotion_result in emotion_results
                ],
                "diary_meta_ids": diary_meta_ids,
            },
            timeout=30,
        )

        if response.status_code == 200:
            task_logger.info("Summary result successfully sent")
        else:
            task_logger.error(
                f"Failed to send summary result: {response.status_code}, {response.text}"
            )

        return {"status": "ok"}
    except Exception as e:

        task_logger.error(f"Summary task failed: {e}")

        if isinstance(e, (TimeoutError, ConnectionError)):
            raise self.retry(exc=e, countdown=15)

        raise e
