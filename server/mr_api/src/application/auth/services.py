from dataclasses import dataclass

from fastapi import Response

from src.adapters.api.auth import schemas
from src.adapters.api.settings import AuthJWT
from src.application import exceptions
from src.application.auth import interfaces as auth_interfaces
from src.application.user import interfaces as user_interfaces
from src.application.utils import (
    hash_password,
    validate_non_empty_fields,
    verify_password,
)


@dataclass
class AuthService:
    """
    Сервис аутентификации пользователей.
    """

    user_repo: user_interfaces.IUserRepository
    token_manager: auth_interfaces.ITokenManager

    async def register_user(
        self,
        user: schemas.CreateUser,
        response: Response,
        authorize: AuthJWT
    ) -> schemas.AuthResponse:
        """
        Регистрирует нового пользователя.

        :param user: Данные нового пользователя для регистрации.
        :param response: Объект ответа FastAPI,
        используется для управления куками.
        :param authorize: Объект аутентификации JWT.

        :return: Ответ с данными пользователя и токенами доступа.

        :raises exceptions.UserExistsException: В случае,
        если пользователь с указанным адресом электронной почты уже существует.
        """

        empty_field = validate_non_empty_fields(user.dict())
        if empty_field:
            raise exceptions.EmptyFieldException(empty_field)

        user_exsist = await self.user_repo.get_user_by_email(user.email)

        if user_exsist:
            raise exceptions.UserExistsException(user.email)

        user.password = hash_password(user.password)

        user_data = await self.user_repo.create_user(user)

        if user_data:
            tokens = self.token_manager.create_tokens(
                user_data.id,
                response,
                authorize
            )

            return schemas.AuthResponse(
                id=user_data.id,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                email=user_data.email,
                access_token=tokens[0],
                refresh_token=tokens[1]
            )

    async def login_user(
        self,
        user: schemas.LoginUser,
        response: Response,
        authorize: AuthJWT
    ) -> schemas.AuthResponse:
        """
        Аутентифицирует пользователя.

        :param user: Данные пользователя для входа.
        :param response: Объект ответа FastAPI,
        используется для управления куками.
        :param authorize: Объект аутентификации JWT.

        :return: Ответ с данными пользователя и токенами доступа.

        :raises exceptions.UserNotFoundException: В случае, если пользователь
        с указанным адресом электронной почты не найден.
        :raises exceptions.InvalidCredentialsException: В случае,
        если указаны неверные учетные данные.
        """

        empty_field = validate_non_empty_fields(user.dict())
        if empty_field:
            raise exceptions.EmptyFieldException(empty_field)

        user_data = await self.user_repo.get_user_by_email(
            user.email
        )

        if user_data is None:
            raise exceptions.UserNotFoundException()

        if not verify_password(user.password, user_data.password):
            raise exceptions.InvalidCredentialsException()

        tokens = self.token_manager.create_tokens(
            user_data.id,
            response,
            authorize
        )

        return schemas.AuthResponse(
            id=user_data.id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            access_token=tokens[0],
            refresh_token=tokens[1]
        )

    # async def refresh_token(
    #     self,
    #     response: Response,
    #     authorize: AuthJWT,
    #     user_id: int
    # ) -> dict[str, str]:
    #     access_token = TokenManager().create_access_token(
    #         authorize,
    #         str(user_id)
    #     )

    #     response.set_cookie(
    #         "access_token",
    #         access_token,
    #         settings.ACCESS_TOKEN_EXPIRES_IN * 60,
    #         settings.ACCESS_TOKEN_EXPIRES_IN * 60,
    #         "/",
    #         None,
    #         False,
    #         True,
    #         "lax"
    #     )

    #     return {
    #         "access_token": access_token
    #     }

    async def logout_user(
        self,
        response: Response,
        authorize: AuthJWT
    ) -> dict[str, str]:
        """
        Осуществляет выход пользователя из системы
        путем удаления текущих токенов.

        :param response: Объект ответа FastAPI,
        используется для управления куками.
        :param authorize: Объект аутентификации JWT,
        используется для удаления текущих токенов.

        :return: Словарь с ключом "status" и значением "success",
        указывающим на успешное завершение операции.
        """
        self.token_manager.delete_tokens(response, authorize)
        return {
            "status": "success"
        }
