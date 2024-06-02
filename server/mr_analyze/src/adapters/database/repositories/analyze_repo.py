from dataclasses import dataclass
from datetime import timedelta

import sqlalchemy as sqla

from src.adapters.database import tables
from src.adapters.database.repositories.base_repo import SABaseRepository
from src.application.analyze import entities, interfaces
from src.application.constants import TimeConstants
from src.application.utils import get_current_dt


@dataclass
class AnalyzeRepository(SABaseRepository, interfaces.IAnalyzeRepository):
    """
    Репозиторий для работы с данными анализа в базе данных.
    """

    async def get_hour_ago_analyze_results(
        self
    ) -> list[entities.AnalyzeReturn | None]:
        """
        Извлекает резульатты анализа за последний час.

        :return: Объект анализа или None, если анализ не найден.
        """
        table: sqla.Table = tables.analyze

        now_dt = get_current_dt(TimeConstants.DEFAULT_TIMEZONE)
        one_hour_ago_dt = now_dt - timedelta(hours=1)

        query: sqla.Select = (
            sqla.select(
                table.c.id,
                table.c.dt,
                table.c.source_type,
                table.c.source_url,
                table.c.entries_analyze,
                table.c.full_analyze,
                table.c.status
            )
            .filter(
                table.c.dt >= one_hour_ago_dt
            )
        ).order_by(table.c.id.desc())

        analyze_results = self.session.execute(query).mappings().all()

        if analyze_results:
            return [entities.AnalyzeReturn(**row) for row in analyze_results]
        return []
