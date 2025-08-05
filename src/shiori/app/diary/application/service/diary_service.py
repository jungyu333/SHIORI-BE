from typing import Optional

from shiori.app.core.database import MongoTransactional
from shiori.app.diary.domain.entity import DiaryBlockVO, DiaryVO, DiaryMetaVO
from shiori.app.diary.domain.repository import DiaryRepository, DiaryMetaRepository
from shiori.app.diary.domain.validator import DiaryMetaValidator
from shiori.app.diary.infra.model import ProseMirror


class DiaryService:
    def __init__(
        self, diary_repo: DiaryRepository, diary_meta_repo: DiaryMetaRepository
    ):
        self._diary_repo = diary_repo
        self._diary_meta_repo = diary_meta_repo

    async def save_diary(
        self,
        *,
        user_id: int,
        diary_meta_id: str,
        date: str,
        content: ProseMirror,
    ) -> tuple[str, bool]:

        diary_blocks = DiaryBlockVO.from_prosemirror(content.model_dump())

        diary = DiaryVO(
            user_id=user_id,
            diary_meta_id=diary_meta_id,
            date=date,
            diary_content=content,
            diary_blocks=diary_blocks,
        )

        diary_document_id, is_created = await self._diary_repo.save_diary(diary=diary)

        return diary_document_id, is_created

    async def save_diary_meta(
        self, *, user_id: int, date: str, title: str
    ) -> str | None:

        DiaryMetaValidator.validate_date_format(date)
        DiaryMetaValidator.validate_title(title)

        diary_meta_vo = DiaryMetaVO(
            user_id=user_id,
            date=date,
            title=title,
        )

        diary_meta_id = await self._diary_meta_repo.save_diary_meta(diary_meta_vo)

        return diary_meta_id

    @MongoTransactional()
    async def upsert_diary(
        self,
        *,
        user_id: int,
        date: str,
        content: ProseMirror,
        title: Optional[str] = "",
    ) -> tuple[str | None, bool | None]:

        diary_meta_id = await self.save_diary_meta(
            user_id=user_id, date=date, title=title
        )

        if diary_meta_id:
            diary_id, is_created = await self.save_diary(
                user_id=user_id,
                diary_meta_id=diary_meta_id,
                date=date,
                content=content,
            )

            return diary_id, is_created

        return None, None
