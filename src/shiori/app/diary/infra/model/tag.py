from sqlalchemy import Integer, String, Float, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from shiori.app.core.database.mixins import TimestampMixin
from shiori.app.core.database.session import Base


class Tag(Base, TimestampMixin):
    __tablename__ = "tags"
    __table_args__ = (
        UniqueConstraint("diary_meta_id", "label", name="uq_diary_meta_label"),
        Index("ix_tags_diary_meta_id", "diary_meta_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(String(20), nullable=False)
    diary_meta_id: Mapped[str] = mapped_column(String(24), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f"<Tag(id={self.id}, label={self.label}, diary_mate_id={self.diary_meta_id}, confidence='{self.confidence}')>"
