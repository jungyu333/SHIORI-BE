from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    code: int = 200
    message: Optional[str] = ""
    data: Optional[T] =  Field(default_factory=dict)
