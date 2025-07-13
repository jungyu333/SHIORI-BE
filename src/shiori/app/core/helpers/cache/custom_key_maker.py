import hashlib
import inspect
from typing import Callable, Any

from shiori.app.core.helpers.cache.base import BaseKeyMaker


class CustomKeyMaker(BaseKeyMaker):
    async def make(
        self,
        *,
        function: Callable,
        prefix: str,
        args: tuple = (),
        kwargs: dict[str, Any] = {},
    ) -> str:
        path = f"{prefix}::{inspect.getmodule(function).__name__}.{function.__name__}"
        key_base = str(args) + str(kwargs)
        key_hash = hashlib.md5(key_base.encode()).hexdigest()

        return f"{path}.{key_hash}"
