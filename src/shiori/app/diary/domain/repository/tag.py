from abc import ABC, abstractmethod

from shiori.app.diary.domain.entity import TagVO


class TagRepository(ABC):

    @abstractmethod
    async def save(self, *, tag: TagVO) -> int:
        pass
