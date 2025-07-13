from abc import abstractmethod, ABC
from typing import Callable, Any


class BaseKeyMaker(ABC):
    @abstractmethod
    async def make(
        self,
        *,
        function: Callable,
        prefix: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> str:
        pass
