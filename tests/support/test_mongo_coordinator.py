from pymongo import MongoClient

from shiori.app.core import get_settings

config = get_settings()


class TestMongoCoordinator:
    __test__ = True

    EXCLUDE_COLLECTIONS = {
        "system.indexes"
    }

    def __init__(self) -> None:
        self.client =  MongoClient(config.MONGO_DB_URL)
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
