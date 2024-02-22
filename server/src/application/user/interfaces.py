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

    # @abstractmethod
    # async def get_user_by_id(self, user_id: int) -> user_schemas.UserRead:
    #     pass
