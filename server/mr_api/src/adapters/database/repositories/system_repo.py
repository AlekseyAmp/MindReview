from dataclasses import asdict, dataclass

import sqlalchemy as sqla

from src.adapters.database import tables
from src.adapters.database.repositories.base_repo import SABaseRepository
from src.application.system import entities, interfaces


@dataclass
class SystemRepository(SABaseRepository, interfaces.ISystemRepository):
    """
    Репозиторий для работы с системной информацией.
    """

    async def save_log(
        self,
        log: entities.LogInput
    ) -> int:
        """
        Сохраняет лог в базе данных.

        :param log: Объект для сохранения.

        :return: Идентификатор лога.
        """

        table: sqla.Table = tables.logs

        query: sqla.Insert = (
            sqla.insert(
                table
            )
            .values(
                asdict(log)
            )
            .returning(
                table.c.id
            )
        )

        log = self.session.execute(query).mappings().one()
        self.session.commit()
        return log

    async def get_all_logs(
        self
    ) -> list[entities.LogReturn | None]:
        """
        Получает все логи приложения.

        :return: Список объектов логов или пустой список,
        если логов нет.
        """

        table: sqla.Table = tables.logs

        query: sqla.Select = (
            sqla.select(
                table.c.id,
                table.c.dt,
                table.c.level,
                table.c.message
            ).order_by(table.c.id.desc())
        )

        logs = self.session.execute(query).mappings().all()

        if logs:
            return [entities.LogReturn(**row) for row in logs]
        return []
