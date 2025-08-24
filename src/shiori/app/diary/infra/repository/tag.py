from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from shiori.app.core.database import session
from shiori.app.diary.domain.entity import TagVO
from shiori.app.diary.domain.repository import TagRepository
from shiori.app.diary.infra.model import Tag


class TagRepositoryImpl(TagRepository):

    async def upsert(self, *, tag: TagVO) -> None:

        model = tag.to_model()

        session.add(model)

        try:
            await session.flush()
        except IntegrityError:
            await session.rollback()
            await session.execute(
                update(Tag)
                .where(
                    Tag.diary_meta_id == model.diary_meta_id,
                    Tag.label == model.label,
                )
                .values(confidence=model.confidence)
            )
