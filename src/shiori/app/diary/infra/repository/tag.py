from shiori.app.core.database import session
from shiori.app.diary.domain.entity import TagVO
from shiori.app.diary.domain.repository import TagRepository


class TagRepositoryImpl(TagRepository):

    async def save(self, *, tag: TagVO) -> int:

        model = tag.to_model()

        session.add(model)

        await session.flush()

        return model.id
