from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    email: str
    password: str
    nickname: Optional[str]
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

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
