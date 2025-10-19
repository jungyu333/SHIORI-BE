from shiori.app.celery.celery_app import celery_app
from shiori.app.diary.application.service import DiaryService


class CreateSummarize:
    def __init__(self, diary_service: DiaryService):
        self._diary_service = diary_service

    async def execute(self, *, user_id: int, start_date: str, end_date: str) -> bool:

        week_diary, diary_meta_ids = await self._diary_service.can_summarize_diary(
            user_id=user_id,
            start=start_date,
            end=end_date,
        )

        if not week_diary:
            return False

        celery_app.send_task(
            "summary_task",
            args=[
                {
                    "user_id": user_id,
                    "start": start_date,
                    "end": end_date,
                    "week_diary": week_diary,
                    "diary_meta_ids": diary_meta_ids,
                }
            ],
            queue="summary-queue",
        )

        return True
