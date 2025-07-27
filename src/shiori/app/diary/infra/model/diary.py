from beanie import Document

from shiori.app.core.database.mixins import MongoTimestampMixin
from shiori.app.diary.domain.entity import ProseMirror, DiaryBlock


class DiaryDocument(Document, MongoTimestampMixin):
    user_id: int
    diary_meta_id: int
    date: str
    diary_content: ProseMirror
    diary_blocks: list[DiaryBlock]

    class Settings:
        name = "diary"
        indexes = [[("user_id", 1), ("diary_meta_id", 1)]]

    class Config:
        arbitrary_types_allowed = True
