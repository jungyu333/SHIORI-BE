from abc import ABC, abstractmethod

from typing import Any


class BaseBackend(ABC):
    @abstractmethod
    async def get(self, *, key: str) -> Any:
        pass

    @abstractmethod
    async def set(self, *, response: Any, key: str, ttl: int = 60) -> None:
        pass

    @abstractmethod
    async def delete_startswith(self, *, value: str) -> None:
        pass
