from shiori.app.diary.application.service import DiaryService
from shiori.app.diary.infra.model import SummaryStatus


class SummarizeResult:
    def __init__(self, *, diary_service: DiaryService):
        self._diary_service = diary_service

    async def execute(
        self,
        *,
        user_id: int,
        start: str,
        end: str,
        reflection: str,
        emotion_results: list[dict],
        diary_meta_ids: list[str],
    ):

        await self._diary_service.upsert_summary_result(
            user_id=user_id,
            start=start,
            end=end,
            reflection=reflection,
            emotion_results=emotion_results,
            diary_meta_ids=diary_meta_ids,
        )

        await self._diary_service.update_summary_status(
            diary_meta_id=diary_meta_ids,
            status=SummaryStatus.completed,
        )
