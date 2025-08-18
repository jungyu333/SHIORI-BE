from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from shiori.app.diary.infra.model import Tag as Tag_Model


@dataclass
class Tag:
    label: str
    confidence: float
    id: Optional[int] = None
    diary_meta_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_model(cls, model: Tag_Model) -> "Tag":
        tag = Tag(
            id=model.id,
            label=model.label,
            confidence=model.confidence,
            diary_meta_id=model.diary_meta_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        return tag

    def to_model(self) -> Tag_Model:
        tag = Tag_Model(
            label=self.label,
            confidence=self.confidence,
            diary_meta_id=self.diary_meta_id,
        )
        return tag
