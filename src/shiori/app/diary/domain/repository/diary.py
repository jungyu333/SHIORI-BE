from abc import ABC, abstractmethod

from shiori.app.diary.domain.entity import DiaryVO


class DiaryRepository(ABC):

    @abstractmethod
    async def save_diary(self, *, diary: DiaryVO) -> str:
        pass
