from abc import ABC, abstractmethod

from shiori.app.diary.domain.entity import DiaryMetaVO


class DiaryMetaRepository(ABC):

    @abstractmethod
    async def save_diary_meta(self, diary_meta: DiaryMetaVO) -> str:
        pass

    @abstractmethod
    async def get_diary_meta_by_date_range(
        self, user_id: int, start_date: str, end_date: str
    ) -> list[DiaryMetaVO]:
        pass
