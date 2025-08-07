from beanie import init_beanie
from pymongo import MongoClient

from shiori.app.core import get_settings
from shiori.app.core.database import mongo_client
from shiori.app.diary.infra.model import DiaryDocument, DiaryMetaDocument

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

        async_db = mongo_client[config.MONGO_DB_NAME]

        print(async_db, 'async_db')
        await init_beanie(database=async_db, document_models=[DiaryDocument, DiaryMetaDocument])