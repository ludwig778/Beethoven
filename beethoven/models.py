from dataclasses import dataclass

from beethoven.core.abstract import AbstractModel


@dataclass
class GridModel(AbstractModel):
    name: str
    data: str
