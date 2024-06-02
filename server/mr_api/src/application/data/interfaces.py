from abc import ABC, abstractmethod

from src.application.data import entities


class IDataRepository(ABC):

    @abstractmethod
    async def get_all_stopwords(self) -> list[entities.StopwordReturn]:
        pass

    @abstractmethod
    async def update_stopword_is_use(
        self,
        stopword_id: int
    ) -> None:
        pass

    @abstractmethod
    async def delete_stopword(
        self,
        stopword_id: int
    ) -> None:
        pass
