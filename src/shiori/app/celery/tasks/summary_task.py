import asyncio

from shiori.app.celery import celery_app
from shiori.app.container import Container
from shiori.app.diary.infra.model import SummaryStatus


@celery_app.task(name="summary_task")
def summary_task(payload: dict):
    container = Container()

    diary_service = container.diary_service()

    user_id = payload["user_id"]
    start = payload["start"]
    end = payload["end"]
    week_diary = payload["week_diary"]
    diary_meta_ids = payload["diary_meta_ids"]

    try:
        asyncio.run(
            diary_service.summarize_diary(
                user_id=user_id,
                start=start,
                end=end,
                week_diary=week_diary,
                diary_meta_ids=diary_meta_ids,
            )
        )
    except Exception as e:
        asyncio.run(
            diary_service.update_summary_status(
                diary_meta_id=diary_meta_ids,
                status=SummaryStatus.failed,
            )
        )
