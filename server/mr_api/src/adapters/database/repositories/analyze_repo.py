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

    async def get_last_analyze_by_user_id(
        self,
        user_id: int
    ) -> entities.AnalyzeReturn | None:
        """
        Получает последний результат анализа из базы данных
        по ID пользователя.

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
                table.c.user_id == user_id
            )
        ).order_by(table.c.dt.desc()).limit(1)

        analyze = self.session.execute(query).mappings().one_or_none()

        if analyze:
            return entities.AnalyzeReturn(**analyze)
        return None

    async def get_all_analyze_result_by_user_id(
        self,
        user_id: int
    ) -> list[entities.AnalyzeReturn | None]:
        pass
        """
        Получает все последние результат анализа из базы данных
        по ID пользователя.

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
                table.c.user_id == user_id
            )
        ).order_by(table.c.id.desc())

        analyze_results = self.session.execute(query).mappings().all()

        if analyze_results:
            return [entities.AnalyzeReturn(**row) for row in analyze_results]
        return []
