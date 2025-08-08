from shiori.app.diary.application.service import DiaryService


class GetDiary:
    def __init__(self, diary_service: DiaryService):
        self._diary_service = diary_service

    async def execute(self, user_id: int, date: str) -> dict | None:

        content = await self._diary_service.get_diary_content(
            user_id=user_id,
            date=date,
        )

        return content
