from typing import List, Union

from pydantic import BaseModel

from beethoven import controllers
from beethoven.models import Degree, Note, Scale


class ChordItem(BaseModel):
    root: Union[Note, Degree]
    name: str

    def __str__(self):
        chord_name = str(self.root)

        if self.name:
            chord_name += " " + self.name.replace("_", " ")

        return chord_name

    def as_chord(self, scale: Scale):
        chord_str = f"{self.root}4"

        if self.name:
            chord_str += f"_{self.name.replace(' ', '_')}"

        return controllers.chord.parse_with_scale_context(chord_str, scale=scale)

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name"),
            root=controllers.utils.parse_root_note_or_degree(data["root"]),
        )

    def dict(self, *args, **kwargs):
        return {"name": self.name, "root": str(self.root)}


class HarmonyItem(BaseModel):
    scale: Scale
    chord_items: List[ChordItem]

    @classmethod
    def from_dict(cls, data):
        return cls(
            scale=controllers.scale.parse(data["scale"]),
            chord_items=[ChordItem.from_dict(item) for item in data["chord_items"]],
        )

    def dict(self, *args, **kwargs):
        # print(2, self, args, kwargs)
        # pp({
        #    "scale": str(self.scale),
        #    "chord_items": [
        #        chord_item.dict()
        #        for chord_item in self.chord_items
        #    ]
        # })
        return {
            "scale": str(self.scale).replace(" ", "_"),
            "chord_items": [chord_item.dict() for chord_item in self.chord_items],
        }


class HarmonyItems(BaseModel):
    items: List[HarmonyItem]

    @classmethod
    def from_list(cls, data_items):
        return cls(items=[HarmonyItem.from_dict(item) for item in data_items])

    def dict(self, *args, **kwargs):
        return [item.dict() for item in self.items]
