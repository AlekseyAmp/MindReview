from dataclasses import dataclass

from src.adapters.api.system import schemas
from src.application import exceptions
from src.application.constants import UserRole
from src.application.user import interfaces as user_interfaces


@dataclass
class SystemService:
    """
    Сервис для работы с системой.
    """

    user_repo: user_interfaces.IUserRepository

    async def get_system_info(
        self,
        user_id: int,
    ) -> schemas.SystemInfoResponse:
        """
        Возвращает информацию о системе.

        :param user_id: ID пользователя.

        :return: Информация о системе.
        """

        # Проверка на роль администратора
        user = await self.user_repo.get_user_info_by_id(user_id)

        if user.role != UserRole.ADMIN.value:
            raise exceptions.NotAdminRoleException

        return schemas.SystemInfoResponse()

    async def get_system_logs(
        self,
        user_id: int,
    ) -> None:
        """
        Возвращает логи приложения.

        :param user_id: ID пользователя.

        :return: Информация о системе.
        """

        # Проверка на роль администратора
        user = await self.user_repo.get_user_info_by_id(user_id)

        if user.role != UserRole.ADMIN.value:
            raise exceptions.NotAdminRoleException

        pass
