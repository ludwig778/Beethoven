from abc import ABC, abstractmethod
from typing import Generator


class AbstractObject(ABC):
    pass


class AbstractGridComponent(AbstractObject):
    @abstractmethod
    def __iter__(self) -> Generator:
        pass
