import json
from dataclasses import dataclass
from typing import Generator

from src.adapters.rpc.manager import RabbitMQManager
from src.application.analyze import interfaces


@dataclass
class ReviewConsumer(interfaces.IReviewСonsumer):
    """
    Класс для получения отзывов на анализ.

    Этот класс предоставляет функциональность
    для получения отзывов на анализ из указанной очереди RabbitMQ.
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

    # async def check_queue_empty(self, queue_name: str) -> list | None:
    #     """
    #     Проверяет, пуста ли указанная очередь.

    #     :param queue_name: Название очереди для проверки.
    #     :return: Список отзывов, если очередь не пуста,
    #     в противном случае None.
    #     """

    #     # TODO: доделать
    #     async with self.channel:
    #         source_queue = await self.channel.declare_queue(queue_name)

    #         reviews = []

    #         async for review_message in source_queue:
    #             reviews.append(review_message)

    #         if reviews:
    #             return None

    async def receive_reviews(self, queue_name: str) -> Generator:
        """
        Получает список отзывов из указанной очереди.

        :param queue_name: Название очереди для получения отзывов.

        :return: Генератор, возвращающий отзывы
        по мере их получения из очереди.
        """
        async with self.channel_pool.acquire() as channel:
            source_queue = await channel.declare_queue(queue_name)
            async for message in source_queue:
                async with message.process():
                    yield json.loads(message.body.decode())
