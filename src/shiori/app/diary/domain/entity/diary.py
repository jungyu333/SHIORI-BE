from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict, Literal, Optional


class Mark(TypedDict):
    type: Literal["bold", "italic", "strike", "underline"]


class TextNode(TypedDict):
    type: Literal["text"]
    text: str
    marks: Optional[list[Mark]]


class NodeAttrs(TypedDict, total=False):
    textAlign: Optional[Literal["left", "center", "right"]]
    level: Optional[int]


class ContentNode(TypedDict):
    type: str
    attrs: Optional[NodeAttrs]
    content: Optional[list[TextNode]]


class ProseMirror(TypedDict):
    type: Literal["doc"]
    content: list[ContentNode]


class DiaryBlock(TypedDict):
    order: int
    type: Literal["paragraph", "heading", "quote", "todo", "divider"]
    content: Optional[str]
    level: Optional[int]
    textAlign: Optional[Literal["left", "center", "right"]]
    marks: Optional[list[Literal["bold", "italic", "strike"]]]
    is_in_quote: Optional[bool]
    parent_type: Optional[str]
    token_length: Optional[int]
    checked: Optional[bool]


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

    def to_model(self):
        pass
