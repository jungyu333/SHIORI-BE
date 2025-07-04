from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: int
    email: str
    password: str
    nickname: Optional[str]
    avatar_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, model):
        pass

    @classmethod
    def to_model(cls, model):
        pass
