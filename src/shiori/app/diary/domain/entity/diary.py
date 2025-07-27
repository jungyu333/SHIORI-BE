from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

from shiori.app.diary.infra.model import DiaryDocument


class Mark(BaseModel):
    type: Literal["bold", "italic", "strike", "underline"]


class TextNode(BaseModel):
    type: Literal["text"]
    text: str
    marks: Optional[list[Mark]] = None


class NodeAttrs(BaseModel):
    textAlign: Optional[Literal["left", "center", "right"]] = None
    level: Optional[int] = None


class ContentNode(BaseModel):
    type: str
    attrs: Optional[NodeAttrs] = None
    content: Optional[list[TextNode]] = None


class ProseMirror(BaseModel):
    type: Literal["doc"]
    content: list[ContentNode]


class DiaryBlock(BaseModel):
    order: int
    type: Literal["paragraph", "heading", "quote", "todo", "divider"]
    content: Optional[str] = None
    level: Optional[int] = None
    textAlign: Optional[Literal["left", "center", "right"]] = None
    marks: Optional[list[Literal["bold", "italic", "strike"]]] = None
    is_in_quote: Optional[bool] = None
    parent_type: Optional[str] = None
    token_length: Optional[int] = None
    checked: Optional[bool] = None


@dataclass
class Diary:
    user_id: int
    diary_meta_id: int
    date: str
    diary_content: ProseMirror
    diary_blocks: list[DiaryBlock]
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
            diary_blocks=model.diary_blocks,
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
            diary_blocks=self.diary_blocks,
            user_id=self.user_id,
        )

        return diary
