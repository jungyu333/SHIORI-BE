from typing import Optional

from shiori.app.diary.application.service import DiaryService
from shiori.app.diary.infra.model import ProseMirror


class UpsertDiary:
    def __init__(self, *, diary_service: DiaryService):
        self._diary_service = diary_service

    async def execute(
        self,
        *,
        user_id: int,
        date: str,
        version: int,
        content: ProseMirror,
        title: Optional[str] = "",
    ) -> tuple[str | None, bool | None]:
        diary_id, is_created = await self._diary_service.upsert_diary(
            user_id=user_id,
            date=date,
            version=version,
            content=content,
            title=title,
        )

        return diary_id, is_created
