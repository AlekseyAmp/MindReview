
from abc import ABC, abstractmethod

from fastapi import Response

from src.adapters.api.settings import AuthJWT


class ITokenManager(ABC):

    @abstractmethod
    def create_tokens(
        self,
        user_id: str,
        response: Response,
        authorize: AuthJWT
    ) -> tuple[str, str]:
        pass

    @abstractmethod
    def delete_tokens(
        self,
        response: Response,
        authorize: AuthJWT
    ) -> None:
        pass
