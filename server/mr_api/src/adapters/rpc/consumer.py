import json
from dataclasses import dataclass
from typing import Generator

from src.adapters.rpc.manager import RabbitMQManager
from src.application.review import interfaces


@dataclass
class AnalyzeConsumer(interfaces.IAnalyzeConsumer):
    """
    Класс для получения результатов анализа.

    Этот класс предоставляет функциональность
    для получения результата анализа из указанной очереди RabbitMQ.
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

    async def receive_analyze_results(
        self,
        queue_name: str
    ) -> Generator:
        """
        Получает результаты анализа из указанной очереди.

        :param queue_name: Название очереди для получения отзывов.

        :return: Генератор, возвращающий результаты анализа
        по мере их получения из очереди.
        """
        async with self.channel_pool.acquire() as channel:
            source_queue = await channel.declare_queue(queue_name)
            async for message in source_queue:
                async with message.process():
                    yield json.loads(message.body.decode())
