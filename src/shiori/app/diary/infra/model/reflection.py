from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from shiori.app.core.database.mixins import TimestampMixin
from shiori.app.core.database.session import Base


class Reflection(Base, TimestampMixin):
    __tablename__ = "reflections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    start_date: Mapped[str] = mapped_column(String(20), nullable=False)
    end_date: Mapped[str] = mapped_column(String(20), nullable=False)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self):
        return f"<Reflection(id={self.id}, start_date={self.start_date}, end_date={self.end_date}, summary_text='{self.summary_text}')>"
