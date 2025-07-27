from shiori.app.diary.domain.entity import DiaryVO
from shiori.app.diary.domain.repository import DiaryRepository
from shiori.app.diary.infra.model import DiaryDocument


class DiaryRepositoryImpl(DiaryRepository):
    async def save_diary(self, diary: DiaryVO) -> str:

        existed_document = await DiaryDocument.find_one(
            DiaryDocument.user_id == diary.user_id,
            DiaryDocument.diary_meta_id == diary.diary_meta_id,
        )

        diary_document = diary.to_model()

        if existed_document:
            diary_document.id = existed_document.id
            await diary_document.replace()
        else:
            await diary_document.insert()

        return str(diary_document.id)
