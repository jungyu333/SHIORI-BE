from sqlalchemy import select

from shiori.app.core.database import session
from shiori.app.diary.domain.entity import DiaryMetaVO
from shiori.app.diary.domain.repository import DiaryMetaRepository
from shiori.app.diary.infra.model import DiaryMeta


class DiaryMetaRepositoryImpl(DiaryMetaRepository):

    async def save_diary_meta(self, *, diary_meta: DiaryMetaVO) -> int:

        diary_meta_model = diary_meta.to_model()

        stmt = select(DiaryMeta).where(DiaryMeta.id == diary_meta_model.id)

        existing_diary_meta = await session.execute(stmt).scalar().first()

        if existing_diary_meta:
            return existing_diary_meta.id

        session.add(diary_meta_model)

        await session.flush()

        return diary_meta_model.id
