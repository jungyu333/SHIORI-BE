from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from shiori.app.diary.domain.entity import DiaryBlockVO
from shiori.app.diary.infra.model import DiaryDocument, ProseMirror


@dataclass
class Diary:
    user_id: int
    diary_meta_id: int
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
            diary_meta_id=model.meta_id,
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

    def to_model(self) -> DiaryDocument:
        diary = DiaryDocument(
            diary_meta_id=self.diary_meta_id,
            date=self.date,
            diary_content=self.diary_content,
            diary_blocks=[block.to_dict() for block in self.diary_blocks],
            user_id=self.user_id,
        )

        return diary
