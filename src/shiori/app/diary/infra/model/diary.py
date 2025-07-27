from typing import Literal, Optional

from beanie import Document
from pydantic import BaseModel

from shiori.app.core.database.mixins import MongoTimestampMixin


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


class DiaryDocument(Document, MongoTimestampMixin):
    user_id: int
    diary_meta_id: int
    date: str
    diary_content: ProseMirror
    diary_blocks: list[DiaryBlock]

    class Settings:
        name = "diary"
        indexes = [{"keys": [("user_id", 1), ("diary_meta_id", 1)], "unique": True}]

    class Config:
        arbitrary_types_allowed = True
