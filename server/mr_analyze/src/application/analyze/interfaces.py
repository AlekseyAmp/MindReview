from abc import ABC, abstractmethod
from typing import Generator


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
    def analyze_sentiment(self, reviews: list[dict]) -> dict[int, float]:
        pass

    @abstractmethod
    def extract_keywords(self, reviews: list[dict]) -> dict[int, list[str]]:
        pass

    @abstractmethod
    def extract_gender_author(self, reviews: list[dict]) -> dict[int, str]:
        pass

    @abstractmethod
    def extract_age_author(self, reviews: list[dict]) -> dict[int, int]:
        pass
