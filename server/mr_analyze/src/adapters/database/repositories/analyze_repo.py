from dataclasses import dataclass

import sqlalchemy as sqla

from src.adapters.database.repositories.base_repo import SABaseRepository
from src.application.analyze import interfaces


@dataclass
class AnalyzeRepository(SABaseRepository, interfaces.IAnalyzeRepository):
    """
    Репозиторий для работы с данными анализа в базе данных.
    """
    pass
