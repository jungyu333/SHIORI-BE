from enum import Enum as PyEnum

from beanie import Document
from pymongo import IndexModel

from shiori.app.core.database.mixins import MongoTimestampMixin


class SummaryStatus(str, PyEnum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class DiaryMetaDocument(Document, MongoTimestampMixin):
    user_id: int
    date: str
    title: str

    summary_status: SummaryStatus = SummaryStatus.pending
    is_archived: bool = False

    class Settings:
        name = "diary-meta"
        indexes = [
            IndexModel(
                [("user_id", 1), ("date", 1)],
                name="ix_diary_meta_user_id_date",
                unique=True,
            )
        ]

    class Config:
        arbitrary_types_check = True
