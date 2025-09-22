from abc import ABC, abstractmethod

from shiori.app.diary.domain.entity import ReflectionVO


class ReflectionRepository(ABC):

    @abstractmethod
    async def upsert(self, *, reflection: ReflectionVO) -> None:
        pass

    @abstractmethod
    async def get(
        self, *, user_id: int, start_date: str, end_date: str
    ) -> ReflectionVO | None:
        pass
