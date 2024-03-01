from dataclasses import dataclass

import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

from src.adapters.rpc.settings import settings


@dataclass
class RabbitMQManager:
    """
    Класс для управления пулами соединений и каналов для RabbitMQ.

    Этот класс обеспечивает методы для получения соединения и канала,
    а также управляет пулами соединений и каналов для повторного использования.
    """

    connection_pool: Pool = None
    channel_pool: Pool = None

    async def get_connection(self) -> AbstractRobustConnection:
        """
        Получает соединение с RabbitMQ.

        :return: Асинхронный объект соединения с RabbitMQ.
        """
        return await aio_pika.connect_robust(
            host=settings.RABBITMQ_HOST,
            port=int(settings.RABBITMQ_PORT),
            login=settings.RABBITMQ_LOGIN,
            password=settings.RABBITMQ_PASSWORD
        )

    async def get_pool_connection(self) -> Pool:
        """
        Получает пул соединений с RabbitMQ.

        :return: Пул соединений с RabbitMQ.
        """
        if self.connection_pool is None:
            self.connection_pool = Pool(self.get_connection)
        return self.connection_pool

    async def get_channel(self) -> aio_pika.Channel:
        """
        Получает канал для взаимодействия с RabbitMQ.

        :return: Асинхронный объект канала для взаимодействия с RabbitMQ.
        """
        async with self.connection_pool.acquire() as connection:
            return await connection.channel()

    async def get_channel_pool(self) -> Pool:
        """
        Получает пул каналов для RabbitMQ.

        :return: Пул каналов для RabbitMQ.
        """
        if self.channel_pool is None:
            self.channel_pool = Pool(self.get_channel)
        return self.channel_pool
