from abc import ABC, abstractmethod

from src.application.collection import entities as collection_entities


class IDataRepository(ABC):

    @abstractmethod
    def get_all_cities(
        self
    ) -> list[collection_entities.City] | None:
        pass

    @abstractmethod
    def get_all_stopwords(
        self
    ) -> list[collection_entities.StopwordReturn] | None:
        pass

    @abstractmethod
    async def save_stopwords(
        self,
        stopwords: list[collection_entities.StopwordInput]
    ) -> None:
        pass
