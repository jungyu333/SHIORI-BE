from functools import wraps

from pymongo.errors import PyMongoError

from shiori.app.core.database import (
    mongo_client,
    set_mongo_session,
    reset_mongo_session,
)


class MongoTransactional:
    def __init__(self, *, session: str = "session"):
        self.session = session

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with await mongo_client.start_session() as session:
                set_mongo_session(session)
                try:
                    kwargs[self.session] = session
                    return await func(*args, **kwargs)
                except PyMongoError as e:
                    raise e
                finally:
                    reset_mongo_session()

        return wrapper
