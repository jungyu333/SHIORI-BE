from typing import Literal, Optional, Union

from beanie import Document
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field
from pymongo import IndexModel

from shiori.app.core.database.mixins import MongoTimestampMixin


class Mark(BaseModel):
    type: Literal["bold", "italic", "strike", "underline", "code"]


class TextNode(BaseModel):
    type: Literal["text"]
    text: str
    marks: Optional[list[Mark]] = None


class NodeAttrs(BaseModel):

    textAlign: Optional[Literal["left", "center", "right"]] = Field(
        default=None, alias="text_align"
    )
    level: Optional[int] = None

    model_config = ConfigDict(populate_by_name=True)


class ContentNode(BaseModel):
    type: str
    attrs: Optional[NodeAttrs] = None

    content: Optional[list[Union[TextNode, "ContentNode"]]] = None


class ProseMirror(BaseModel):
    type: Literal["doc"]
    content: list[ContentNode]


class DiaryDocument(Document, MongoTimestampMixin):
    user_id: int
    diary_meta_id: ObjectId
    date: str
    diary_content: ProseMirror
    diary_blocks: list[dict]

    class Settings:
        name = "diary"
        indexes = [
            IndexModel(
                [("user_id", 1), ("diary_meta_id", 1)],
                unique=True,
                name="idx_user_meta",
            ),
            IndexModel(
                [("user_id", 1), ("date", 1)],
                unique=True,
                name="idx_user_date",
            ),
        ]

    class Config:
        arbitrary_types_allowed = True
