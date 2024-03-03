import logging
from dataclasses import asdict, dataclass

from src.application.analyze import interfaces as analyze_interface
from src.application.collection import interfaces as collection_interfaces


@dataclass
class CollectionService:
    """
    Сервис для сбора различных данных с проанализированных отзывов.
    """

    analyze_repo: analyze_interface.IAnalyzeRepository
    data_repo: collection_interfaces.IDataRepository

    pass
