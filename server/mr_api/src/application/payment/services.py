from dataclasses import dataclass

from src.adapters.logger.settings import logger
from src.application.constants import LogLevel, TimeConstants
from src.application.system import interfaces as system_interfaces
from src.application.system.entities import LogInput
from src.application.user import interfaces as user_interfaces
from src.application.utils import get_current_dt


@dataclass
class PaymentService:
    """
    Сервис для работы с системной информацией.
    """

    user_repo: user_interfaces.IUserRepository
    system_repo: system_interfaces.ISystemRepository

    async def set_premium(
        self,
        user_id: int
    ) -> dict[str, str]:
        """
        Возвращает информацию о системе.

        :param user_id: ID пользователя.

        :return: Информация о системе.
        """

        await self.user_repo.set_user_premium(user_id)

        log_info = LogInput(
            dt=get_current_dt(TimeConstants.DEFAULT_TIMEZONE),
            level=LogLevel.INFO.value,
            message=(
                "Пользователь стал премиум-пользователем. "
                f"(user_id: {user_id}) "
            )
        )
        logger.info(log_info.message)
        await self.system_repo.save_log(log_info)

        return {"message": "Вы стали премиум-пользователем."}
