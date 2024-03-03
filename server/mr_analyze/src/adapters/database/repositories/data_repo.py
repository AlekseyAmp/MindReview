from dataclasses import dataclass

import sqlalchemy as sqla

from src.adapters.database import tables
from src.adapters.database.repositories.base_repo import SABaseRepository
from src.application.collection import entities, interfaces


@dataclass
class DataRepository(SABaseRepository, interfaces.IDataRepository):
    """
    Репозиторий для работы с данными для тренировки модели.
    """
    def get_all_cities(self) -> list[entities.City] | None:
        """
        Получает список всех городов из базы данных.

        :return: Список объектов городов (entities.City), если найдены,
                в противном случае None.
        """
        table: sqla.Table = tables.cities

        query: sqla.Select = (
            sqla.select(
                table.c.id,
                table.c.raw_name,
                table.c.original_name
            )
        )

        result: sqla.MappingResult = self.session.execute(query).mappings()
        return [entities.City(**row) for row in result]
