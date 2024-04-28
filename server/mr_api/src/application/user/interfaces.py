from abc import ABC, abstractmethod

from src.adapters.api.auth import schemas as auth_schemas
from src.application.user import entities


class IUserRepository(ABC):

    @abstractmethod
    async def create_user(
        self,
        user: auth_schemas.CreateUser
    ) -> entities.User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> entities.User | None:
        pass

    @abstractmethod
    async def get_user_info_by_id(
        self,
        user_id: int
    ) -> entities.UserInfo | None:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> entities.User | None:
        pass

    @abstractmethod
    async def get_all_users(self) -> list[entities.User | None]:
        pass

    @abstractmethod
    async def update_user_by_id(
        self,
        user: entities.UserUpdate
    ) -> entities.User:
        pass

    @abstractmethod
    async def delete_user_by_id(
        self,
        user_id: int
    ) -> int:
        pass
