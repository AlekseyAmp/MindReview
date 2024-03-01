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
        user_id: int,
        analyze: entities.AnalyzeInput
    ) -> entities.AnalyzeReturn:
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


class ExcelManager(ABC):

    @abstractmethod
    def load_data(self, file: typing.BinaryIO) -> Worksheet:
        pass
