from abc import abstractmethod, ABC
from typing import Callable


class BaseKeyMaker(ABC):
    @abstractmethod
    async def make(self, *, function: Callable, prefix: str) -> str:
        pass
