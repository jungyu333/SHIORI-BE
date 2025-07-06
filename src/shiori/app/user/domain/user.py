from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: int
    email: str
    password: str
    nickname: Optional[str]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, model) -> "User":
        user = User(
            id=model.id,
            email=model.email,
            password=model.password,
            nickname=model.nickname,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

        return user

    @classmethod
    def to_model(cls, user):
        pass
