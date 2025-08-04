from abc import ABC, abstractmethod

from shiori.app.diary.domain.entity import DiaryMetaVO


class DiaryMetaRepository(ABC):

    @abstractmethod
    async def save_diary_meta(self, diary_meta: DiaryMetaVO) -> int:
        pass
