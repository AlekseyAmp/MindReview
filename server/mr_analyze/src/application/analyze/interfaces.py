from abc import ABC, abstractmethod
from typing import Generator

from src.application.collection import entities


class IAnalyzeRepository(ABC):
    pass


class IReviewСonsumer(ABC):

    # @abstractmethod
    # async def check_queue_empty(self, queue_name: str) -> list | None:
    #     pass

    @abstractmethod
    async def receive_reviews(self, queue_name: str) -> Generator:
        pass


class IAnalyzeProducer(ABC):

    @abstractmethod
    async def send_analyze_results(
        self,
        analyze_results: dict,
        queue_name: str
    ) -> None:
        pass


class INLPService(ABC):

    @abstractmethod
    def analyze_sentiment(
        self,
        reviews: list[dict]
    ) -> dict[int, tuple[str, float]]:
        pass

    @abstractmethod
    def extract_keywords(
        self,
        reviews: list[dict],
        keywords_stopwords: set[str]
    ) -> dict[int, list[str | None]]:
        pass

    @abstractmethod
    def extract_gender_author(
        self,
        reviews: list[dict]
    ) -> dict[int, str | None]:
        pass

    @abstractmethod
    def extract_years(
        self,
        reviews: list[dict]
    ) -> dict[int, list[int | None]]:
        pass

    @abstractmethod
    def extract_cities(
        self,
        reviews: list[dict],
        all_cities: list[entities.City],
        cities_stopwords: set[str]
    ) -> dict[int, set[str | None]]:
        pass
