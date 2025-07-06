from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ....core.database.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(30), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, nickname='{self.nickname}', email='{self.email}')>"
