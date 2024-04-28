from dataclasses import asdict, dataclass

from async_lru import alru_cache

from src.adapters.api.user import schemas
from src.application import exceptions
from src.application.constants import UserRole
from src.application.user import interfaces as user_interfaces
from src.application.utils import datetime_to_json

# user/get/{id}
# user/get_all
# user/edit/{id}
# user/delete/{id}


@dataclass
class UserService:
    """
    Сервис для работы с пользователями.
    """

    user_repo: user_interfaces.IUserRepository

    def __hash__(self) -> int:
        return hash(id(self))

    @alru_cache
    async def get_user(
        self,
        user_id: int
    ) -> schemas.UserResponse | None:
        """
        Возвращает информацию о пользователе.

        :param user_id: ID запрашиваемоего пользователя.
        :param current_user_id: ID пользователя.

        :return: Информация о пользователе.
        """

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
        self
    ) -> None:
        pass

    async def delete_user(
        self,
        user_id: int
    ) -> None:
        pass
