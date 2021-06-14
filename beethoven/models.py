from beethoven.repository.mongo import grid_part_collection


class GridPart:
    def __init__(self, name, text=None, **kwargs):
        self.name = name

        if not text:
            raise Exception("Text must be set")

        self.text = text

    @classmethod
    def create(cls, name, **kwargs):
        if not (obj := cls.get(name)):
            obj = cls(name, **kwargs)

            grid_part_collection.insert_one(obj.to_dict())

        return obj

    @classmethod
    def list(cls, **kwargs):
        return [
            cls(**ingr)
            for ingr in grid_part_collection.find(kwargs)
        ]

    @classmethod
    def get(cls, name):
        grid_part = grid_part_collection.find_one({"name": name})

        if grid_part:
            return cls(**grid_part)

    def update(self, **kwargs):
        self_data = self.to_dict()
        new_data = {**self_data, **kwargs}

        if self_data != new_data:
            grid_part_collection.update_one({"name": self.name}, {"$set": new_data})

            self.__dict__.update(new_data)

    def delete(self):
        return grid_part_collection.delete_one({"name": self.name})

    def copy(self):
        return self.__class__(**self.to_dict())

    def to_dict(self):
        return {
            "name": self.name,
            "text": self.text
        }

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name} {self.text}>"
