from beanie import init_beanie
from pymongo import MongoClient

from shiori.app.core import get_settings

config = get_settings()


class TestMongoCoordinator:
    __test__ = False

    EXCLUDE_COLLECTIONS = {
        "system.indexes"
    }

    def __init__(self) -> None:
        self.client =  MongoClient(config.MONGO_DB_URL, serverSelectionTimeoutMS=1000)
        self.db = self.client.get_database(config.MONGO_DB_NAME)

    def truncate_all(self) -> None:
        collection_names = self.db.list_collection_names()

        for name in collection_names:
            if name not in self.EXCLUDE_COLLECTIONS:
                self.db[name].delete_many({})

    def drop_all(self) -> None:
        collection_names = self.db.list_collection_names()
        for name in collection_names:
            if name not in self.EXCLUDE_COLLECTIONS:
                self.db.drop_collection(name)

    async def init_beanie_odm(self) -> None:

        from pymongo import AsyncMongoClient
        client = AsyncMongoClient(config.MONGO_DB_URL)
        async_db = client[config.MONGO_DB_NAME]
        await init_beanie(database=async_db, document_models=[])