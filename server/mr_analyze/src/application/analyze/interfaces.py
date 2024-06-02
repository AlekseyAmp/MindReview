from abc import ABC, abstractmethod
from typing import Generator

from src.application.analyze import entities as analyze_entities
from src.application.collection import entities as collection_entities


class IAnalyzeRepository(ABC):

    @abstractmethod
    async def get_hour_ago_analyze_results(
        self
    ) -> list[analyze_entities.AnalyzeReturn | None]:
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
        all_cities: list[collection_entities.City],
        cities_stopwords: set[str]
    ) -> dict[int, set[str | None]]:
        pass
