from __future__ import annotations

from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shiori.app.core.database.mixins import TimestampMixin
from shiori.app.core.database.session import Base


class Reflection(Base, TimestampMixin):
    __tablename__ = "reflections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    start_date: Mapped[str] = mapped_column(String(20), nullable=False)
    end_date: Mapped[str] = mapped_column(String(20), nullable=False)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="reflections")

    def __repr__(self):
        return f"<Reflection(id={self.id}, start_date={self.start_date}, end_date={self.end_date}, summary_text='{self.summary_text}')>"
