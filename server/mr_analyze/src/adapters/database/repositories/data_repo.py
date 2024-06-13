from dataclasses import asdict, dataclass

import sqlalchemy as sqla
from sqlalchemy.dialects.postgresql import insert as psql_insert

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

        result: sqla.MappingResult = self.session.execute(
            query
        ).mappings().all()

        return [entities.City(**row) for row in result]

    def get_all_stopwords(self) -> list[entities.StopwordReturn] | None:
        """
        Получает список всех стоп-слов из базы данных.

        :return: Список объектов стоп-слов (entities.StopwordReturn),
        если найдены, в противном случае None.
        """
        table: sqla.Table = tables.stopwords

        query: sqla.Select = (
            sqla.select(
                table.c.id,
                table.c.dt,
                table.c.word,
                table.c.use
            )
        )
            
        result: sqla.MappingResult = self.session.execute(
            query
        ).mappings().all()

        return [entities.StopwordReturn(**row) for row in result]

    async def save_stopwords(
        self,
        stopwords: list[entities.StopwordInput]
    ) -> None:
        """
        Сохраняет стоп-слова в базу данных.

        :param stopwords: Список стоп-слов.
        """

        table: sqla.Table = tables.stopwords

        query: psql_insert = (
            psql_insert(
                table
            )
            .values(
                [
                    asdict(stopword)
                    for stopword in stopwords
                ]
            )
        )

        do_nothing_query = query.on_conflict_do_nothing(
            index_elements=['word']
        )

        self.session.execute(do_nothing_query)
        self.session.commit()
