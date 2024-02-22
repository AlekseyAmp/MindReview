from fastapi import APIRouter, Depends, Response

from src.adapters.api.auth import schemas
from src.adapters.api.auth.dependencies import (
    check_user_authenticated,
    get_auth_service,
)
from src.adapters.api.settings import AuthJWT
from src.application.auth.services import AuthService

router = APIRouter()


@router.post(
    path="/register_user",
    response_model=schemas.AuthResponse,
    dependencies=[Depends(check_user_authenticated)]
)
async def register_user(
    user: schemas.CreateUser,
    response: Response,
    authorize: AuthJWT = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
) -> schemas.AuthResponse:
    return await auth_service.register_user(user, response, authorize)


@router.post(
    path="/login_user",
    response_model=schemas.AuthResponse,
    dependencies=[Depends(check_user_authenticated)],
)
async def login_user(
    user: schemas.LoginUser,
    response: Response,
    authorize: AuthJWT = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
) -> schemas.AuthResponse:
    return await auth_service.login_user(user, response, authorize)


# @router.post(
#     path="/refresh_token",
#     response_model=dict[str, str],
# )
# async def refresh_token(
#     response: Response,
#     authorize: AuthJWT = Depends(),
#     user_id: int = Depends(get_user_id),
#     auth_service: AuthService = Depends(get_auth_service)
# ) -> dict[str, str]:
#     return await auth_service.refresh_token(
#         response,
#         authorize,
#         user_id
#     )


@router.post(
    path="/logout_user",
    response_model=dict[str, str],
)
async def logout_user(
    response: Response,
    authorize: AuthJWT = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
) -> dict[str, str]:
    return await auth_service.logout_user(response, authorize)
