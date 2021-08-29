from abc import ABC, abstractmethod
from typing import Any, Generator, List


class AbstractObject(ABC):
    pass


class AbstractGridComponent(AbstractObject):
    @abstractmethod
    def __iter__(self) -> Generator:
        pass


class AbstractModel(ABC):
    pass


class AbstractRepository(ABC):
    @abstractmethod
    def __init__(self, **kwargs: Any):
        raise NotImplementedError

    @abstractmethod
    def add(self, model: AbstractModel):
        raise NotImplementedError

    @abstractmethod
    def get(self, reference) -> AbstractModel:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[AbstractModel]:
        raise NotImplementedError

    @abstractmethod
    def update(self, model: AbstractModel) -> List[AbstractModel]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, reference):
        raise NotImplementedError

    @abstractmethod
    def delete_all(self):
        raise NotImplementedError
