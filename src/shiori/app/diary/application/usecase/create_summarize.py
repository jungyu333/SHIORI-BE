from shiori.app.diary.application.service import DiaryService


class CreateSummarize:
    def __init__(self, diary_service: DiaryService):
        self._diary_service = diary_service

    async def execute(self, *, user_id: int, start_date: str, end_date: str) -> bool:

        result = await self._diary_service.summarize_diary(
            user_id=user_id,
            start=start_date,
            end=end_date,
        )

        return result
