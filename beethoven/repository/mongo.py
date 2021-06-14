from pymongo import MongoClient

from beethoven.settings import MONGO_CONFIG, TEST


class MongoRepository:
    def __init__(self, **config):
        self.config = config

        self.connect()

    def connect(self):
        self._client = MongoClient(
            self.get_uri().format(**self.config)
        )
        self.database = getattr(self._client, self.config.get("database"))

    def get_uri(self):
        if self.config.get("srv_mode"):
            return "mongodb+srv://{username}:{password}@{host}/{database}?retryWrites=true&w=majority"

        return "mongodb://{username}:{password}@{host}:{port}/{database}?authSource=admin"

    def get_collection(self, name):
        return getattr(
            self.database,
            ("test_" if TEST else "") + name
        )

    def drop(self, name):
        return self.get_collection(name).drop()


mongo_repo = MongoRepository(
    **MONGO_CONFIG
)

grid_part_collection = mongo_repo.get_collection("grid_part")
