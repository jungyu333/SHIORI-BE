from shiori.app.core.database.mongo_session import get_mongo_session
from shiori.app.diary.domain.entity import DiaryMetaVO
from shiori.app.diary.domain.repository import DiaryMetaRepository
from shiori.app.diary.infra.model import DiaryMetaDocument


class DiaryMetaRepositoryImpl(DiaryMetaRepository):

    async def save_diary_meta(self, *, diary_meta: DiaryMetaVO) -> str:

        session = get_mongo_session()

        existing_meta = await DiaryMetaDocument.find_one(
            DiaryMetaDocument.user_id == diary_meta.user_id,
            DiaryMetaDocument.date == diary_meta.date,
            session=session,
        )

        diary_meta_document = diary_meta.to_model()

        if existing_meta:
            diary_meta_document.id = existing_meta.id
            await diary_meta_document.replace(session=session)
            return str(existing_meta.id)

        await diary_meta_document.insert(session=session)
        return str(diary_meta_document.id)
