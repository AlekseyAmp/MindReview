from fastapi_jwt_auth.exceptions import MissingTokenError
from sqlalchemy.orm import Session

from fastapi import Depends

from src.adapters.api.settings import AuthJWT
from src.adapters.database.repositories import UserRepository
from src.adapters.database.sa_session import get_session
from src.application import exceptions
from src.application.user.services import UserService


def get_user_id(authorize: AuthJWT = Depends()) -> str:
    try:
        authorize.jwt_required()
        user_id = authorize.get_jwt_subject()
        return int(user_id)
    except MissingTokenError:
        raise exceptions.NotAuthenticatedException


def get_user_repo(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repo)
) -> UserService:
    return UserService(user_repo)
