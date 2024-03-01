from dataclasses import asdict, dataclass

import sqlalchemy as sqla

from src.adapters.database import tables
from src.adapters.database.repositories.base_repo import SABaseRepository
from src.application.review import entities, interfaces


@dataclass
class AnalyzeRepository(SABaseRepository, interfaces.IAnalyzeRepository):
    """
    Репозиторий для работы с данными анализа в базе данных.
    """
    async def save_analyze(
        self,
        analyze: entities.AnalyzeInput
    ) -> entities.AnalyzeReturn:
        table: sqla.Table = tables.analyze

        query: sqla.Insert = (
            sqla.insert(
                table
            )
            .values(
                asdict(analyze)
            )
            .returning(
                table.c.id,
                table.c.dt,
                table.c.source_type,
                table.c.source_url,
                table.c.entries_analyze,
                table.c.full_analyze,
                table.c.status
            )
        )

        analyze = self.session.execute(query).mappings().one()
        self.session.commit()
        return entities.AnalyzeReturn(**analyze)
