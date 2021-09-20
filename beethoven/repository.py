import json
from dataclasses import asdict
from pathlib import Path

from beethoven.core.abstract import AbstractRepository
from beethoven.mongo import mongo_instance
from beethoven.utils.deepget import deepget


class JsonRepository(AbstractRepository):
    def __init__(self, **kwargs):
        self.path = self._setup_file(kwargs.get("path"))
        self.model = kwargs.get("model")
        self.table = kwargs.get("table")

    @staticmethod
    def _setup_file(raw_path: str) -> Path:
        path = Path(raw_path)

        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            path.touch(exist_ok=True)

        return path

    def _read(self):
        with open(self.path, "r") as fd:
            data = fd.read()

        if data:
            return json.loads(data)
        else:
            return {}

    def _write(self, data):
        with open(self.path, "w") as fd:
            json.dump(data, fd)

    def add(self, model):
        json_data = self._read()

        if self.table not in json_data:
            json_data[self.table] = {}

        if data := deepget(json_data, [self.table, model.name]):
            new_data = asdict(model)

            if data != new_data:
                return self.update(model)

        else:
            data = asdict(model)

            json_data[self.table][model.name] = data

            self._write(json_data)

            return True

    def get(self, reference):
        json_data = self._read()

        if (data := deepget(json_data, [self.table, reference])) and self.model:
            return self.model(**data)

    def list(self, **kwargs):
        table_data = self._read().get(self.table) or {}

        return [self.model(**data) for data in table_data.values()]

    def update(self, model):
        json_data = self._read()

        if self.table not in json_data:
            json_data[self.table] = {}

        if deepget(json_data, [self.table, model.name]):
            json_data[self.table][model.name] = asdict(model)

            self._write(json_data)

            return True

        return False

    def delete(self, reference):
        json_data = self._read()

        if deepget(json_data, [self.table, reference]):
            json_data[self.table].pop(reference)

            self._write(json_data)

            return True

        return False

    def delete_all(self):
        json_data = self._read()
        json_data[self.table] = {}
        self._write(json_data)


class MongoRepository(AbstractRepository):
    def __init__(self, **kwargs):
        self.model = kwargs.get("model")
        self.collection = mongo_instance.get_database().get_collection(
            kwargs.get("collection")
        )

    def add(self, model):
        if obj := self.get(model.name):
            data = asdict(obj)
            new_data = asdict(model)

            if data != new_data:
                return self.update(model)

        else:
            self.collection.insert_one(asdict(model))

            return True

    def get(self, reference):
        data = self.collection.find_one({"name": reference})

        if data and self.model:
            data.pop("_id")

            return self.model(**data)

    def list(self, **kwargs):
        return [
            self.model(**data)
            for data in self.collection.find(kwargs)
            if data.pop("_id")
        ]

    def update(self, model):
        result = self.collection.update_one(
            {"name": model.name}, {"$set": asdict(model)}
        )

        return bool(result.modified_count)

    def delete(self, reference):
        result = self.collection.delete_one({"name": reference})

        return bool(result.deleted_count)

    def delete_all(self):
        self.collection.drop()

    drop = delete_all
