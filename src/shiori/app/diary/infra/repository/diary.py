from beanie.operators import And
from bson import ObjectId

from shiori.app.core.database.mongo_session import get_mongo_session
from shiori.app.diary.domain.entity import DiaryVO
from shiori.app.diary.domain.repository import DiaryRepository
from shiori.app.diary.infra.model import DiaryDocument


class DiaryRepositoryImpl(DiaryRepository):
    async def save_diary(self, *, diary: DiaryVO) -> tuple[str, bool]:

        session = get_mongo_session()

        existed_document = await DiaryDocument.find_one(
            DiaryDocument.user_id == diary.user_id,
            DiaryDocument.diary_meta_id == ObjectId(diary.diary_meta_id),
            session=session,
        )

        diary_document = DiaryDocument(
            diary_meta_id=ObjectId(diary.diary_meta_id),
            date=diary.date,
            diary_content=diary.diary_content,
            diary_blocks=[block.to_dict() for block in diary.diary_blocks],
            user_id=diary.user_id,
        )

        if existed_document:
            diary_document.id = existed_document.id
            await diary_document.replace(session=session)
            return str(diary_document.id), False
        else:
            await diary_document.insert(session=session)
            return str(diary_document.id), True

    async def get_diary_by_date(self, *, user_id: int, date: str) -> DiaryVO | None:

        session = get_mongo_session()

        existed_document = await DiaryDocument.find_one(
            DiaryDocument.date == date,
            DiaryDocument.user_id == user_id,
            session=session,
        )

        if existed_document:
            diary_vo = DiaryVO.from_model(existed_document)
            return diary_vo

        return None

    async def get_diary_by_date_range(
        self, *, user_id: int, start_date: str, end_date: str
    ) -> list[DiaryVO]:

        session = get_mongo_session()

        diary_docs = (
            await DiaryDocument.find(
                And(
                    DiaryDocument.user_id == user_id,
                    DiaryDocument.date >= start_date,
                    DiaryDocument.date <= end_date,
                ),
                session=session,
            )
            .sort("date")
            .to_list(7)
        )

        return [DiaryVO.from_model(diary_doc) for diary_doc in diary_docs]
