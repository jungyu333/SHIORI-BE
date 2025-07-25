import asyncio
import os
from uuid import uuid4

import pytest
import pytest_asyncio

os.environ["ENV"] = "test"

from shiori.app.core.database.session import reset_session_context
from shiori.app.core.database.session import session as db_session
from shiori.app.core.database.session import set_session_context
from shiori.app.core.database import reset_mongo_session

from tests.support.test_mongo_coordinator import TestMongoCoordinator
from tests.support.test_db_coordinator import TestDbCoordinator

test_db_coordinator = TestDbCoordinator()
test_mongo_coordinator = TestMongoCoordinator()


@pytest.fixture(scope="function", autouse=True)
def session_context():
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    yield
    reset_session_context(context=context)


@pytest.fixture(scope="session", autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def session():
    test_db_coordinator.apply_alembic()
    yield db_session
    await db_session.remove()
    test_db_coordinator.truncate_all()


@pytest_asyncio.fixture(scope="function")
async def init_beanie_once():
    await test_mongo_coordinator.init_beanie_odm()


@pytest.fixture(scope="function")
def mongo_test_context(request):
    if "mongo" not in request.keywords:
        yield
        return

    request.getfixturevalue("init_beanie_once")

    yield
    reset_mongo_session()

    test_mongo_coordinator.truncate_all()
