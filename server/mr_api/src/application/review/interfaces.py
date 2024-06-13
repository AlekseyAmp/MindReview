import typing
from abc import ABC, abstractmethod
from typing import Generator

from openpyxl.worksheet.worksheet import Worksheet

from fastapi import WebSocket

from src.application.review import entities


class IAnalyzeRepository(ABC):

    @abstractmethod
    async def save_analyze(
        self,
        analyze: entities.AnalyzeInput
    ) -> entities.AnalyzeReturn:
        pass

    @abstractmethod
    async def get_analyze_by_id(
        self,
        analyze_id: int,
        user_id: int
    ) -> entities.AnalyzeReturn | None:
        pass

    @abstractmethod
    async def get_last_analyze_by_user_id(
        self,
        user_id: int
    ) -> entities.AnalyzeReturn | None:
        pass

    @abstractmethod
    async def get_all_analyze_result_by_user_id(
        self,
        user_id: int
    ) -> list[entities.AnalyzeReturn | None]:
        pass


class IReviewProducer(ABC):

    @abstractmethod
    async def send_reviews(
        self,
        reviews: list[dict],
        queue_name: str
    ) -> None:
        pass


class IAnalyzeConsumer(ABC):

    @abstractmethod
    async def receive_analyze_results(
        self,
        queue_name: str
    ) -> Generator:
        pass


class IWebSocketManager(ABC):

    @abstractmethod
    async def add_websocket(
        self,
        client_id: int,
        websocket: WebSocket
    ) -> None:
        pass

    @abstractmethod
    def remove_websocket(self, client_id: int) -> None:
        pass

    @abstractmethod
    async def send_message(
        self,
        client_id: int,
        message: str
    ) -> None:
        pass


class IExcelManager(ABC):

    @abstractmethod
    def load_data(self, file: typing.BinaryIO) -> Worksheet:
        pass

    @abstractmethod
    def prepare_data_for_analyze(
        self,
        ws: Worksheet
    ) -> list[entities.ReviewTemplate]:
        pass

    @abstractmethod
    def create_analyze_report(
        self,
        short_analyze: list,
        full_analyze: list
    ) -> str:
        pass


class IReviewsParser(ABC):

    @abstractmethod
    def fetch_wildberries_reviews(
        self,
        reviews_id: int
    ) -> list[entities.ReviewTemplate] | None:
        pass
