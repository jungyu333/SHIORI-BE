from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class SummaryStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


@dataclass
class DiaryMeta:
    id: int
    user_id: int
    date: str
    title: str = ""
    summary_status: SummaryStatus = SummaryStatus.pending
    is_archived: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def mark_summary_completed(self):
        self.summary_status = SummaryStatus.completed

    def mark_summary_failed(self):
        self.summary_status = SummaryStatus.failed

    def archive(self):
        self.is_archived = True

    def unarchive(self):
        self.is_archived = False

    @classmethod
    def from_model(cls, model) -> "DiaryMeta":
        diary_meta = DiaryMeta(
            id=model.id,
            user_id=model.user_id,
            date=model.date,
            title=model.title,
            summary_status=model.summary_status,
            is_archived=model.is_archived,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        return diary_meta

    def to_model(self):
        pass
