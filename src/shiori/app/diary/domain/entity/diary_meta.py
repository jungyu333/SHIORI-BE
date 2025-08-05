from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from shiori.app.diary.infra.model import SummaryStatus, DiaryMetaDocument


@dataclass
class DiaryMeta:
    user_id: int
    date: str
    title: str = ""
    summary_status: SummaryStatus = SummaryStatus.pending
    is_archived: bool = False
    id: Optional[str] = None
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
            id=str(model.id),
            user_id=model.user_id,
            date=model.date,
            title=model.title,
            summary_status=model.summary_status,
            is_archived=model.is_archived,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        return diary_meta

    def to_model(self) -> DiaryMetaDocument:
        diary_mate = DiaryMetaDocument(
            user_id=self.user_id,
            date=self.date,
            title=self.title,
            summary_status=self.summary_status,
            is_archived=self.is_archived,
        )
        return diary_mate
