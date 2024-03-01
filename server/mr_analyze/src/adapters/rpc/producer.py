import json
from dataclasses import dataclass

import aio_pika

from src.adapters.rpc import RabbitMQManager
from src.application.analyze import interfaces


@dataclass
class AnalyzeProducer(interfaces.IAnalyzeProducer):
    """
    Класс для отправки результатов анализа.

    Этот класс предоставляет функциональность
    для отправки результата анализа в указанную очередь RabbitMQ.
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

    async def send_analyze_results(
        self,
        analyze_results: dict,
        queue_name: str
    ) -> None:
        """
        Отправляет результаты анализа в указанную очередь.

        :param analyze_result: Результаты анализа.
        :param queue_name: Название очереди для отправки результата анализа.
        """
        analyze_results_json = json.dumps(analyze_results, ensure_ascii=False)
        async with self.channel_pool.acquire() as channel:
            await channel.default_exchange.publish(
                aio_pika.Message(body=analyze_results_json.encode()),
                routing_key=queue_name
            )
