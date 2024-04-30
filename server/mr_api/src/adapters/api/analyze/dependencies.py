from typing import Generator

from sqlalchemy.orm import Session

from fastapi import Depends

from src.adapters.database.repositories import (  # noqa
    AnalyzeRepository,
    SystemRepository,
    UserRepository,
)
from src.adapters.database.sa_session import get_session
from src.adapters.excel.manager import ExcelManager
from src.adapters.notify.websocket import WebSocketManager
from src.adapters.requests.reviews import ReviewsParser
from src.adapters.rpc import AnalyzeConsumer, RabbitMQManager, ReviewProducer
from src.application.review.services import (
    ResultAnalyzeService,
    ReviewProcessingService,
)


def get_analyze_repo(
    session: Session = Depends(get_session)
) -> AnalyzeRepository:
    return AnalyzeRepository(session)


def get_system_repo(
    session: Session = Depends(get_session)
) -> SystemRepository:
    return SystemRepository(session)


def get_user_repo(
    session: Session = Depends(get_session)
) -> UserRepository:
    return UserRepository(session)


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


def get_reviews_parser() -> ReviewsParser:
    return ReviewsParser()


def get_review_processing_service(
    analyze_repo: AnalyzeRepository = Depends(get_analyze_repo),
    system_repo: SystemRepository = Depends(get_system_repo),
    user_repo: UserRepository = Depends(get_user_repo),
    review_producer: ReviewProducer = Depends(get_review_producer),
    analyze_consumer: AnalyzeConsumer = Depends(get_analyze_consumer),
    websocket_manager: WebSocketManager = Depends(get_websocket_manager),
    excel_manager: ExcelManager = Depends(get_excel_manager),
    reviews_parser: ReviewsParser = Depends(get_reviews_parser)
) -> ReviewProcessingService:
    return ReviewProcessingService(
        analyze_repo,
        system_repo,
        user_repo,
        review_producer,
        analyze_consumer,
        websocket_manager,
        excel_manager,
        reviews_parser
    )


def get_result_analyze_service(
    analyze_repo: AnalyzeRepository = Depends(get_analyze_repo),
    system_repo: SystemRepository = Depends(get_system_repo),
    user_repo: UserRepository = Depends(get_user_repo),
    excel_manager: ExcelManager = Depends(get_excel_manager)
) -> ResultAnalyzeService:
    return ResultAnalyzeService(
        analyze_repo,
        system_repo,
        user_repo,
        excel_manager
    )
