from fastapi_jwt_auth.exceptions import MissingTokenError

from fastapi import Depends

from src.adapters.api.settings import AuthJWT
from src.application import exceptions


def get_user_id(authorize: AuthJWT = Depends()) -> str:
    try:
        authorize.jwt_required()
        user_id = authorize.get_jwt_subject()
        return int(user_id)
    except MissingTokenError:
        raise exceptions.NotAuthenticatedException
