from datetime import datetime, timezone

from beanie import before_event, Insert, Update
from pydantic import Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class MongoTimestampMixin:
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    @before_event(
        Insert,
        Update,
    )
    def update_timestamp(self):
        now = utc_now()
        if not self.created_at:
            self.created_at = now
        self.updated_at = now
