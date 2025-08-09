from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from shiori.app.diary.infra.model import ProseMirror
from .diary_block import DiaryBlock as DiaryBlockVO


@dataclass
class Diary:
    user_id: int
    diary_meta_id: str
    date: str
    diary_content: ProseMirror
    diary_blocks: list[DiaryBlockVO]
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_model(cls, model) -> "Diary":
        diary = Diary(
            id=str(model.id),
            diary_meta_id=str(model.diary_meta_id),
            date=model.date,
            diary_content=model.diary_content,
            diary_blocks=[
                DiaryBlockVO.from_dict(block) for block in model.diary_blocks
            ],
            user_id=model.user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        return diary
