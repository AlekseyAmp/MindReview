from typing import Generator

from sqlalchemy.orm import Session

from fastapi import Depends

from src.adapters.database.repositories.analyze_repo import AnalyzeRepository
from src.adapters.database.sa_session import get_session
from src.adapters.excel.manager import ExcelManager
from src.adapters.notify.websocket import WebSocketManager
from src.adapters.rpc import AnalyzeConsumer, RabbitMQManager, ReviewProducer
from src.application.review.services import ReviewProcessingService


def get_analyze_repo(
    session: Session = Depends(get_session)
) -> AnalyzeRepository:
    return AnalyzeRepository(session)


async def get_io_manager() -> RabbitMQManager:
    return RabbitMQManager()


async def get_review_producer(
    io_manager: RabbitMQManager = Depends(get_io_manager)
) -> Generator:
    async with ReviewProducer(io_manager) as review_producer:
        yield review_producer


async def get_analyze_consumer(
    io_manager: RabbitMQManager = Depends(get_io_manager)
) -> Generator:
    async with AnalyzeConsumer(io_manager) as analyze_consumer:
        yield analyze_consumer


def get_websocket_manager() -> WebSocketManager:
    return WebSocketManager()


def get_excel_manager() -> ExcelManager:
    return ExcelManager()


def get_review_processing_service(
    analyze_repo: AnalyzeRepository = Depends(get_analyze_repo),
    review_producer: ReviewProducer = Depends(get_review_producer),
    analyze_consumer: AnalyzeConsumer = Depends(get_analyze_consumer),
    websocket_manager: WebSocketManager = Depends(get_websocket_manager),
    excel_manager: ExcelManager = Depends(get_excel_manager)
) -> ReviewProcessingService:
    return ReviewProcessingService(
        analyze_repo,
        review_producer,
        analyze_consumer,
        websocket_manager,
        excel_manager
    )
