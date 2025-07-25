from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from enum import Enum
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.sql.expression import Delete, Insert, Update

from shiori.app.core.config import get_settings

setting = get_settings()

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


class EngineType(Enum):
    WRITER = "writer"
    READER = "reader"


engines = {
    EngineType.WRITER: create_async_engine(setting.WRITER_DB_URL, pool_recycle=3600),
    EngineType.READER: create_async_engine(setting.READER_DB_URL, pool_recycle=3600),
}


class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines[EngineType.WRITER].sync_engine
        else:
            return engines[EngineType.READER].sync_engine


_async_session_factory = async_sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=False,
)

session = async_scoped_session(
    session_factory=_async_session_factory, scopefunc=get_session_context
)


class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def session_factory() -> AsyncGenerator[AsyncSession, None]:
    _session = _async_session_factory()
    try:
        yield _session
    finally:
        await _session.close()
