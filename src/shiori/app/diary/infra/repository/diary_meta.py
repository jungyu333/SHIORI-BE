from beanie.operators import And

from shiori.app.core.database.mongo_session import get_mongo_session
from shiori.app.diary.domain.entity import DiaryMetaVO
from shiori.app.diary.domain.repository import DiaryMetaRepository
from shiori.app.diary.infra.model import DiaryMetaDocument, SummaryStatus


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

    async def get_diary_meta_by_date_range(
        self, *, user_id: int, start_date: str, end_date: str
    ) -> list[DiaryMetaVO]:

        session = get_mongo_session()

        diary_meta_docs = await DiaryMetaDocument.find(
            And(
                DiaryMetaDocument.user_id == user_id,
                DiaryMetaDocument.date >= start_date,
                DiaryMetaDocument.date <= end_date,
            ),
            session=session,
        ).to_list()

        return [
            DiaryMetaVO.from_model(diary_meta_doc) for diary_meta_doc in diary_meta_docs
        ]

    async def update_summary_status_by_meta_id(
        self, diary_meta_id: list[str], status: SummaryStatus
    ) -> None:

        session = get_mongo_session()

        await DiaryMetaDocument.update_many(
            filter={"_id": {"$in": diary_meta_id}},
            update={"$set": {"summary_status": status.value}},
            session=session,
        )
