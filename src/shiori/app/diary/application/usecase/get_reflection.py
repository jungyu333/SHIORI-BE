from shiori.app.diary.application.service import DiaryService

from shiori.app.diary.domain.entity import ReflectionVO


class GetReflection:
    def __init__(self, diary_service: DiaryService):
        self._diary_service = diary_service

    async def execute(
        self, *, user_id: int, start_date: str, end_date: str
    ) -> ReflectionVO | None:

        result = await self._diary_service.get_reflection(
            user_id=user_id,
            start=start_date,
            end=end_date,
        )

        return result
