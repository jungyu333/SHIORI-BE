from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Optional

from beanie import init_beanie
from fastapi import FastAPI
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.client_session import ClientSession

from shiori.app.core import get_settings

config = get_settings()

mongo_client = AsyncMongoClient(config.MONGO_DB_URL)
mongo_db: AsyncDatabase = mongo_client[config.MONGO_DB_NAME]


_mongo_session: ContextVar[Optional[ClientSession]] = ContextVar(
    "_mongo_session", default=None
)


def set_mongo_session(session: ClientSession) -> None:
    _mongo_session.set(session)


def get_mongo_session() -> Optional[ClientSession]:
    return _mongo_session.get()


def reset_mongo_session() -> None:
    _mongo_session.set(None)


async def init_mongo() -> None:
    await init_beanie(database=mongo_db, document_models=[])


@asynccontextmanager
async def lifespan_context(app: FastAPI):
    await init_mongo()
    yield
