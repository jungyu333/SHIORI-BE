from abc import ABC, abstractmethod

from shiori.app.diary.domain.entity import ReflectionVO


class ReflectionRepository(ABC):

    @abstractmethod
    async def upsert(self, *, reflection: ReflectionVO) -> int | None:
        pass
