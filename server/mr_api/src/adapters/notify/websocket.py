from dataclasses import dataclass

from fastapi import WebSocket

from src.application.review import interfaces


@dataclass
class WebSocketManager(interfaces.IWebSocketManager):
    """
    Менеджер для управления WebSocket-соединениями.

    Этот класс управляет WebSocket-соединениями
    путем их добавления, удаления
    и отправки сообщений подключенным клиентам.
    """

    active_websockets = {}

    async def add_websocket(
        self,
        client_id: int,
        websocket: WebSocket
    ) -> None:
        """
        Добавляет WebSocket-соединение в менеджер.

        :param client_id: Идентификатор клиента,
        связанный с WebSocket-соединением.
        :param websocket: WebSocket-соединение для добавления.
        """
        await websocket.accept()
        self.active_websockets[client_id] = websocket

    def remove_websocket(
        self,
        client_id: int
    ) -> None:
        """
        Удаляет WebSocket-соединение из менеджера.

        :param client_id: Идентификатор клиента,
        связанный с WebSocket-соединением.
        """
        del self.active_websockets[client_id]

    async def send_message(
        self,
        client_id: int,
        message: str
    ) -> None:
        """
        Отправляет сообщение через WebSocket-соединение,
        связанное с указанным идентификатором клиента.

        Если идентификатор клиента не найден в активных соединениях,
        сообщение не отправляется.

        :param client_id: Идентификатор клиента,
        связанный с WebSocket-соединением.
        :param message: Сообщение для отправки.
        """
        websocket = self.active_websockets.get(client_id)
        if websocket:
            await websocket.send_message(message)
