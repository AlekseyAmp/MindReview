from dataclasses import dataclass

from async_lru import alru_cache

from fastapi import Response

from src.adapters.api.settings import AuthJWT
from src.adapters.api.user import schemas
from src.adapters.logger.settings import logger
from src.application import exceptions
from src.application.constants import LogLevel, TimeConstants, UserRole
from src.application.system import interfaces as system_interfaces
from src.application.system.entities import LogInput
from src.application.user import entities
from src.application.user import interfaces as user_interfaces
from src.application.utils import (
    datetime_to_json,
    get_current_dt,
    hash_password,
    validate_non_empty_fields,
)


@dataclass
class UserService:
    """
    Сервис для работы с пользователями.
    """

    user_repo: user_interfaces.IUserRepository
    system_repo: system_interfaces.ISystemRepository

    def __hash__(self) -> int:
        return hash(id(self))

    @alru_cache
    async def get_user(
        self,
        current_user_id: int,
        user_id: int
    ) -> schemas.UserResponse | None:
        """
        Возвращает информацию о пользователе.

        :param current_user_id: ID текущего пользователя.
        :param user_id: ID запрашиваемоего пользователя.

        :return: Информация о пользователе.
        """

        # Проверка на роль администратора
        check_admin_user = await self.user_repo.get_user_info_by_id(
            current_user_id
        )
        if check_admin_user.role != UserRole.ADMIN.value:
            if current_user_id != user_id:
                raise exceptions.NoAccessException

        # Проверка на существование пользователя
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise exceptions.UserNotFoundException

        return schemas.UserResponse(
            id=user.id,
            dt=datetime_to_json(user.dt),
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            role=user.role,
            is_premium=user.is_premium
        )

    @alru_cache
    async def get_all_users(
        self,
        user_id: int
    ) -> schemas.UsersResponse:
        """
        Возвращает всех пользователей.

        :param user_id: ID пользователя.

        :return: Список пользователей.
        """

        # Проверка на роль администратора
        user = await self.user_repo.get_user_info_by_id(user_id)

        if user.role != UserRole.ADMIN.value:
            raise exceptions.NotAdminRoleException

        users = await self.user_repo.get_all_users()

        # Преобразование даты dt
        for user in users:
            user.dt = datetime_to_json(user.dt)

        users = [
            schemas.UserResponse(
                id=user.id,
                dt=user.dt,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                role=user.role,
                is_premium=user.is_premium
            )
            for user in users
        ]

        return schemas.UsersResponse(
            users=users,
        )

    async def edit_user(
        self,
        update_user: schemas.UpdateUser,
        current_user_id: int,
        user_id: int
    ) -> dict[str, str]:
        """
        Редактирует информацию о пользователе.

        :param update_user: Объект обновления информации о пользователе.
        :param current_user_id: ID текущего пользователя.
        :param user_id: ID пользователя.

        :return: Объект обновленной информации о пользователе.
        """

        empty_field = validate_non_empty_fields(update_user.dict())
        if empty_field:
            raise exceptions.EmptyFieldException(empty_field)

        # Проверка на роль администратора
        check_admin_user = await self.user_repo.get_user_info_by_id(
            current_user_id
        )
        if check_admin_user.role != UserRole.ADMIN.value:
            if current_user_id != user_id:
                raise exceptions.NoAccessException

        # Проверка на существование пользователя
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise exceptions.UserNotFoundException

        # Если пользователь меняет email,
        # проверяем, что новый email не существует у другого пользователя
        if update_user.email != user.email:
            user_exist = await self.user_repo.get_user_by_email(
                update_user.email
            )
            if user_exist and user_exist.id != user_id:
                raise exceptions.UserExistsException(update_user.email)

        user_update = entities.UserUpdate(
            id=user.id,
            first_name=update_user.first_name,
            last_name=update_user.last_name,
            email=update_user.email,
        )

        user_data = await self.user_repo.update_user_by_id(
            user_update
        )

        log_info = LogInput(
            dt=get_current_dt(TimeConstants.DEFAULT_TIMEZONE),
            level=LogLevel.INFO.value,
            message=(
                "Информация о пользователе обновлена. "
                f"(user_id: {user_data.id}) "
            )
        )
        logger.info(log_info.message)
        await self.system_repo.save_log(log_info)

        return {"message": "Информация обновлена."}

    async def delete_user(
        self,
        response: Response,
        authorize: AuthJWT,
        current_user_id: int,
        user_id: int
    ) -> dict[str, str]:
        """
        Удаляет пользователя.

        :param current_user_id: ID текущего пользователя.
        :param user_id: ID пользователя.

        :return: Сообщение о удалении.
        """

        # Проверка на роль администратора
        check_admin_user = await self.user_repo.get_user_info_by_id(
            current_user_id
        )
        if check_admin_user.role != UserRole.ADMIN.value:
            if current_user_id != user_id:
                raise exceptions.NoAccessException

        # Проверка на существование пользователя
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise exceptions.UserNotFoundException

        await self.user_repo.delete_user_by_id(user_id)

        log_info = LogInput(
            dt=get_current_dt(TimeConstants.DEFAULT_TIMEZONE),
            level=LogLevel.INFO.value,
            message=(
                "Пользователь удален. "
                f"(user_id: {user_id}) "
            )
        )
        logger.info(log_info.message)
        await self.system_repo.save_log(log_info)

        if check_admin_user.role != UserRole.ADMIN.value:
            authorize.unset_jwt_cookies()
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")

        return {"message": "Вы удалили свой аккаунт."}
