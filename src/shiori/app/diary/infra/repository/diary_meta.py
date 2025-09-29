from beanie.operators import And, Set, In, Inc
from bson import ObjectId

from shiori.app.core.database.mongo_session import get_mongo_session
from shiori.app.diary.domain.entity import DiaryMetaVO
from shiori.app.diary.domain.repository import DiaryMetaRepository
from shiori.app.diary.infra.model import DiaryMetaDocument, SummaryStatus


class DiaryMetaRepositoryImpl(DiaryMetaRepository):

    async def save_diary_meta(self, *, diary_meta: DiaryMetaVO) -> str | None:

        session = get_mongo_session()

        existing_meta = await DiaryMetaDocument.find_one(
            DiaryMetaDocument.user_id == diary_meta.user_id,
            DiaryMetaDocument.date == diary_meta.date,
            session=session,
        )

        if existing_meta:
            result = DiaryMetaDocument.find_one(
                DiaryMetaDocument.id == existing_meta.id,
                DiaryMetaDocument.version == existing_meta.version,
                session=session,
            ).update(
                Set(
                    {
                        DiaryMetaDocument.title: diary_meta.title,
                        DiaryMetaDocument.summary_status: diary_meta.summary_status,
                        DiaryMetaDocument.is_archived: diary_meta.is_archived,
                    }
                ),
                Inc({DiaryMetaDocument.version: 1}),
            )

            if result.matched_count == 0:

                return None

            return str(existing_meta.id)

        diary_meta_document = diary_meta.to_model()
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

        object_ids = [ObjectId(id_str) for id_str in diary_meta_id]

        await DiaryMetaDocument.find(
            In(DiaryMetaDocument.id, object_ids), session=session
        ).update_many(Set({DiaryMetaDocument.summary_status: status}), session=session)
