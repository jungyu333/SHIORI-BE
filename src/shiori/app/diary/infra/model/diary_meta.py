from sqlalchemy import Integer, ForeignKey, String, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shiori.app.core.database.mixins import TimestampMixin
from shiori.app.core.database.session import Base
from shiori.app.diary.domain.entity import SummaryStatus
from shiori.app.user.infra.model.user import User


class DiaryMeta(Base, TimestampMixin):
    __tablename__ = "diary_meta"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="diary_meta_list")

    date: Mapped[str] = mapped_column(String(30), nullable=False)
    title: Mapped[str] = mapped_column(String(255), default="")
    summary_status: Mapped[SummaryStatus] = mapped_column(
        Enum(SummaryStatus), default=SummaryStatus.pending
    )
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"<DiaryMeta(id={self.id}, user_id='{self.user_id}', date='{self.date}', title='{self.title}', summary_status='{self.summary_status}', is_archived='{self.is_archived}')>"
