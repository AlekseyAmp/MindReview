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
        """
        Сохраняет анализ в базе данных.

        :param analyze: Объект анализа для сохранения.

        :return: Объект возвращаемого анализа.
        """
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

    async def get_analyze_by_id(
        self,
        analyze_id: int,
        user_id: int
    ) -> entities.AnalyzeReturn | None:
        """
        Получает анализ из базы данных по его ID.

        :param analyze_id: ID анализа.
        :param user_id: ID пользователя.

        :return: Объект анализа или None, если анализ не найден.
        """
        table: sqla.Table = tables.analyze

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
                table.c.id == analyze_id,
                table.c.user_id == user_id
            )
        )
        analyze = self.session.execute(query).mappings().one_or_none()

        if analyze:
            return entities.AnalyzeReturn(**analyze)
        return None
