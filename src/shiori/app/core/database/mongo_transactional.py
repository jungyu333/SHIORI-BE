from functools import wraps

from pymongo.errors import PyMongoError

from shiori.app.core.database import (
    mongo_client,
    set_mongo_session,
    reset_mongo_session,
)


class MongoTransactional:
    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            async with mongo_client.start_session() as session:
                set_mongo_session(session)
                try:
                    await session.start_transaction()
                    result = await func(*args, **kwargs)
                    await session.commit_transaction()
                    return result
                except PyMongoError as e:
                    await session.abort_transaction()
                    raise e
                finally:
                    reset_mongo_session()

        return wrapper
