from abc import ABC, abstractmethod

from shiori.app.diary.domain.entity import DiaryVO


class DiaryRepository(ABC):

    @abstractmethod
    async def save_diary(self, *, diary: DiaryVO) -> tuple[str, bool]:
        pass

    @abstractmethod
    async def get_diary_by_date(self, *, user_id: int, date: str) -> DiaryVO | None:
        pass
