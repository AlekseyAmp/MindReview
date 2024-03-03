from abc import ABC, abstractmethod

from src.application.collection import entities


class IDataRepository(ABC):

    @abstractmethod
    def get_all_cities(self) -> list[entities.City] | None:
        pass
