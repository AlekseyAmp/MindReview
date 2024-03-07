from dataclasses import dataclass
from datetime import timedelta

from fastapi import Response

from src.adapters.api.settings import AuthJWT, settings
from src.application.auth import interfaces


@dataclass
class TokenManager(interfaces.ITokenManager):
    def create_tokens(
        self,
        user_id: str,
        headers: dict[str, str | bool],
        response: Response,
        authorize: AuthJWT
    ) -> tuple[str, str]:
        """
        Создает и устанавливает новые токены доступа
        и обновления для пользователя,
        а также устанавливает куки в ответе.

        :param user_id: Идентификатор пользователя.
        :param response: Объект ответа FastAPI, используется для установки кук.
        :param authorize: Объект аутентификации JWT.

        :return: Кортеж с токеном доступа и токеном обновления.
        """
        access_token_expires = timedelta(
            minutes=int(settings.ACCESS_TOKEN_EXPIRES_IN)
        )
        refresh_token_expires = timedelta(
            minutes=int(settings.REFRESH_TOKEN_EXPIRES_IN)
        )

        access_token = authorize.create_access_token(
            subject=str(user_id),
            headers=headers,
            expires_time=access_token_expires
        )
        refresh_token = authorize.create_refresh_token(
            subject=str(user_id),
            headers=headers,
            expires_time=refresh_token_expires
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=access_token_expires,
            expires=access_token_expires,
            path="/",
            secure=True,
            httponly=True,
            samesite="lax"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=refresh_token,
            expires=refresh_token,
            path="/",
            secure=True,
            httponly=True,
            samesite="lax"
        )

        return access_token, refresh_token

    def delete_tokens(
        self,
        response: Response,
        authorize: AuthJWT
    ) -> None:
        """
        Удаляет токены доступа и обновления из кук ответа.

        :param response: Объект ответа FastAPI, используется для удаления кук.
        :param authorize: Объект аутентификации JWT.

        :return: None
        """
        authorize.unset_jwt_cookies()
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return None
