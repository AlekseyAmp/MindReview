from sqlalchemy.orm import Session

from fastapi import Depends, Request

from src.adapters.database.repositories.user_repo import UserRepository
from src.adapters.database.sa_session import get_session
from src.application import exceptions
from src.application.auth.services import AuthService


def get_user_repo(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repo),
) -> AuthService:
    return AuthService(
        user_repo
    )


def check_user_authenticated(request: Request) -> None:
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if access_token or refresh_token:
        raise exceptions.AlreadyAuthenticatedException()
