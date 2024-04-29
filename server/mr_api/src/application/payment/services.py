from dataclasses import dataclass

from fastapi import Response

from src.adapters.api.settings import AuthJWT
from src.adapters.logger.settings import logger
from src.application import exceptions
from src.application.auth import interfaces as auth_interfaces
from src.application.constants import LogLevel, TimeConstants, UserRole
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
    token_manager: auth_interfaces.ITokenManager

    async def set_premium(
        self,
        user_id: int,
        response: Response,
        authorize: AuthJWT
    ) -> dict[str, str]:
        """
        Возвращает информацию о системе.

        :param user_id: ID пользователя.

        :return: Информация о системе.
        """

        user = await self.user_repo.get_user_by_id(user_id)

        if user.is_premium or user.role == UserRole.ADMIN.value:
            raise exceptions.UserAlreadyPremium

        await self.user_repo.set_user_premium(user_id)

        token_headers = {
            "is_premium": user.is_premium,
            "role": user.role
        }
        self.token_manager.create_tokens(
            user.id,
            token_headers,
            response,
            authorize
        )

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
