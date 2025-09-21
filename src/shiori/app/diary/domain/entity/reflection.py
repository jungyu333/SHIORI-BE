from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from shiori.app.diary.infra.model import Reflection as Reflection_Model


@dataclass
class Reflection:
    user_id: int
    start_date: str
    end_date: str
    summary_text: str
    id: Optional[int] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_model(cls, model: Reflection_Model) -> "Reflection":
        reflection = Reflection(
            id=model.id,
            user_id=model.user_id,
            start_date=model.start_date,
            end_date=model.end_date,
            summary_text=model.summary_text,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        return reflection

    def to_model(self) -> Reflection_Model:
        reflection = Reflection_Model(
            user_id=self.user_id,
            start_date=self.start_date,
            end_date=self.end_date,
            summary_text=self.summary_text,
        )
        return reflection
