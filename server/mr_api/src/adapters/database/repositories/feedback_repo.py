from dataclasses import asdict, dataclass

import sqlalchemy as sqla

from src.adapters.database import tables
from src.adapters.database.repositories.base_repo import SABaseRepository
from src.application.feedback import entities, interfaces


@dataclass
class FeedbackRepository(SABaseRepository, interfaces.IFeedbackRepository):
    """
    Репозиторий для работы с обратной связью.
    """

    async def save_feedback(
        self,
        feedback: entities.FeedbackInput
    ) -> entities.FeedbackReturn:
        """
        Сохраняет запись обратной связи от пользователя в базе данных.

        :param feedback: Объект для сохранения.

        :return: FeedbackReturn.
        """

        table: sqla.Table = tables.feedbacks

        query: sqla.Insert = (
            sqla.insert(
                table
            )
            .values(
                asdict(feedback)
            )
            .returning(
                table.c.id,
                table.c.dt,
                table.c.response_dt,
                table.c.message,
                table.c.response,
                table.c.sender_email,
                table.c.recipient_email
            )
        )

        feedback = self.session.execute(query).mappings().one()
        self.session.commit()
        return entities.FeedbackReturn(**feedback)

    async def update_feedback(
        self,
        feedback: entities.FeedbackUpdate
    ) -> entities.FeedbackReturn:
        """
        Обновляет запись обратной связи от пользователя в базе данных.
        (Ответ от СП)

        :param feedback: Объект для обновления.

        :return: FeedbackReturn.
        """

        table: sqla.Table = tables.feedbacks

        query: sqla.Update = (
            sqla.update(
                table
            )
            .filter(
                table.c.id == feedback.id
            )
            .values(
                response_dt=feedback.response_dt,
                response=feedback.response
            )
            .returning(
                table.c.id,
                table.c.dt,
                table.c.response_dt,
                table.c.message,
                table.c.response,
                table.c.sender_email,
                table.c.recipient_email
            )
        )

        feedback = self.session.execute(query).mappings().one()
        self.session.commit()
        return entities.FeedbackReturn(**feedback)

    async def get_feedback_by_id(
        self,
        feedback_id
    ) -> entities.FeedbackReturn | None:
        """
        Получает запись обратной связи по ID.

        :param feedback_id: ID обратной связи.

        :return: Объект обратной связи или None,
        если обратная связь не найдена.
        """
        table: sqla.Table = tables.feedbacks

        query: sqla.Select = (
            sqla.select(
                table.c.id,
                table.c.dt,
                table.c.response_dt,
                table.c.message,
                table.c.response,
                table.c.sender_email,
                table.c.recipient_email
            )
            .filter(
                table.c.id == feedback_id
            )
        )

        feedback = self.session.execute(query).mappings().one_or_none()

        if feedback:
            return entities.FeedbackReturn(**feedback)
        return None

    async def get_all_answered_feedbacks(
        self
    ) -> list[entities.FeedbackReturn | None]:
        """
        Получает все обратные связи, на которые уже был получен ответ.

        :return: Список объектов обратной связи или пустой список,
        если обратных связей нет.
        """
        table: sqla.Table = tables.feedbacks

        query: sqla.Select = (
            sqla.select(
                table.c.id,
                table.c.dt,
                table.c.response_dt,
                table.c.message,
                table.c.response,
                table.c.sender_email,
                table.c.recipient_email
            )
            .filter(
                table.c.response.isnot(None)
            ).order_by(table.c.id.desc())
        )

        feedbacks = self.session.execute(query).mappings().all()

        if feedbacks:
            return [entities.FeedbackReturn(**row) for row in feedbacks]
        return []

    async def get_all_unanswered_feedbacks(
        self
    ) -> list[entities.FeedbackReturn | None]:
        """
        Получает все обратные связи, на которые еще не был получен ответ.

        :return: Список объектов обратной связи или пустой список,
        если обратных связей нет.
        """
        table: sqla.Table = tables.feedbacks

        query: sqla.Select = (
            sqla.select(
                table.c.id,
                table.c.dt,
                table.c.response_dt,
                table.c.message,
                table.c.response,
                table.c.sender_email,
                table.c.recipient_email
            )
            .filter(
                table.c.response.is_(None)
            ).order_by(table.c.id.desc())
        )

        feedbacks = self.session.execute(query).mappings().all()

        if feedbacks:
            return [entities.FeedbackReturn(**row) for row in feedbacks]
        return []
