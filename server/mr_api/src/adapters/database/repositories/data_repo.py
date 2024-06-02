from dataclasses import dataclass

import sqlalchemy as sqla

from src.adapters.database import tables
from src.adapters.database.repositories.base_repo import SABaseRepository
from src.application.data import entities, interfaces


@dataclass
class DataRepository(SABaseRepository, interfaces.IDataRepository):
    """
    Репозиторий для работы с данными для тренировки модели.
    """

    async def get_all_stopwords(self) -> list[entities.StopwordReturn]:
        """
        Получает список всех стоп-слов из базы данных.

        :return: Список объектов стоп-слов (entities.StopwordReturn).
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

    async def update_stopword_is_use(
        self,
        stopword_id: int
    ) -> None:
        """
        Обновляет статус стоп-слова.

        :param stopword_id: ID стоп-слова.

        :return: None
        """
        table: sqla.Table = tables.stopwords

        query: sqla.Update = (
            sqla.update(table)
            .where(table.c.id == stopword_id)
            .values(use=True)
        )

        self.session.execute(query)
        self.session.commit()

    async def delete_stopword(
        self,
        stopword_id: int
    ) -> None:
        """
        Удаляет стоп-слово.

        :param stopword_id: ID стоп-слова.

        :return: None
        """
        table: sqla.Table = tables.stopwords

        query: sqla.Delete = (
            sqla.delete(table)
            .where(table.c.id == stopword_id)
        )

        self.session.execute(query)
        self.session.commit()
