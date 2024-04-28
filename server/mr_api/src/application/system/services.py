from dataclasses import asdict, dataclass

from async_lru import alru_cache

from src.adapters.api.system import schemas
from src.application import exceptions
from src.application.constants import UserRole
from src.application.system import interfaces as system_interfaces
from src.application.user import interfaces as user_interfaces
from src.application.utils import datetime_to_json


@dataclass
class SystemService:
    """
    Сервис для работы с системной информацией.
    """

    system_repo: system_interfaces.ISystemRepository
    user_repo: user_interfaces.IUserRepository

    def __hash__(self) -> int:
        return hash(id(self))

    @alru_cache
    async def get_system_info(
        self,
        user_id: int
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

    @alru_cache
    async def get_all_logs(
        self,
        user_id: int
    ) -> schemas.LogsResponse:
        """
        Возвращает логи приложения.

        :param user_id: ID пользователя.

        :return: Список логов.
        """

        # Проверка на роль администратора
        user = await self.user_repo.get_user_info_by_id(user_id)

        if user.role != UserRole.ADMIN.value:
            raise exceptions.NotAdminRoleException

        all_logs = await self.system_repo.get_all_logs()

        # Преобразование даты dt
        for log in all_logs:
            log.dt = datetime_to_json(log.dt)

        logs = [
            schemas.LogResponse(**asdict(log))
            for log in all_logs
        ]

        return schemas.LogsResponse(
            logs=logs,
        )
