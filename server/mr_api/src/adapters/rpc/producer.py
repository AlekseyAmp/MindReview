import json
from dataclasses import dataclass

import aio_pika

from src.adapters.rpc.manager import RabbitMQManager
from src.application.review import interfaces


@dataclass
class ReviewProducer(interfaces.IReviewProducer):
    """
    Класс для отправки отзывов на анализ.

    Этот класс предоставляет функциональность
    для отправки отзывов на анализ в указанную очередь RabbitMQ.
    """

    io_manager: RabbitMQManager

    async def __aenter__(self):
        """
        Метод для создания контекстного менеджера.
        """
        self.connection_pool = await self.io_manager.get_pool_connection()
        self.channel_pool = await self.io_manager.get_channel_pool()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """
        Метод для закрытия подключения при выходе из контекстного менеджера.
        """
        await self.connection_pool.close()

    async def send_reviews(
        self,
        reviews: list[dict],
        queue_name: str
    ) -> None:
        """
        Отправляет список отзывов в указанную очередь.

        :param reviews: Список отзывов.
        :param queue_name: Название очереди для отправки результата анализа.
        """
        reviews_json = json.dumps(reviews, ensure_ascii=False)
        async with self.channel_pool.acquire() as channel:
            await channel.default_exchange.publish(
                aio_pika.Message(body=reviews_json.encode()),
                routing_key=queue_name
            )
