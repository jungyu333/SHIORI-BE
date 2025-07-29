from shiori.app.core.database import MongoTransactional, Transactional
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

    @MongoTransactional()
    async def save_diary(
        self,
        *,
        user_id: int,
        diary_meta_id: int,
        date: str,
        content: ProseMirror,
    ) -> str:

        diary_blocks = DiaryBlockVO.from_prosemirror(content.model_dump())

        diary = DiaryVO(
            user_id=user_id,
            diary_meta_id=diary_meta_id,
            date=date,
            diary_content=content,
            diary_blocks=diary_blocks,
        )

        diary_document_id = await self._diary_repo.save_diary(diary=diary)

        return diary_document_id

    @Transactional()
    async def save_diary_meta(self, *, user_id: int, date: str, title: str) -> None:

        DiaryMetaValidator.validate_date_format(date)
        DiaryMetaValidator.validate_title(title)

        diary_meta_vo = DiaryMetaVO(
            user_id=user_id,
            date=date,
            title=title,
        )

        await self._diary_meta_repo.save_diary_meta(diary_meta_vo)
