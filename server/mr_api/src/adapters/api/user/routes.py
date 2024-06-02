from fastapi import APIRouter, Depends, Response

from src.adapters.api.settings import AuthJWT
from src.adapters.api.user import schemas
from src.adapters.api.user.dependencies import get_user_id, get_user_service
from src.application.user.services import UserService

router = APIRouter()


@router.get(
    path="/{user_id}",
    response_model=schemas.UserResponse
)
async def get_user(
    user_id: int,
    current_user_id: int = Depends(get_user_id),
    user_service: UserService = Depends(
        get_user_service
    ),
) -> schemas.UserResponse:
    return await user_service.get_user(current_user_id, user_id)


@router.get(
    path="",
    response_model=list[schemas.UserResponse | None]
)
async def get_all_users(
    user_id: int = Depends(get_user_id),
    user_service: UserService = Depends(
        get_user_service
    ),
) -> list[schemas.UserResponse | None]:
    return await user_service.get_all_users(user_id)


@router.patch(
    path="/{user_id}",
    response_model=dict[str, str]
)
async def edit_user(
    update_user: schemas.UpdateUser,
    user_id: int,
    current_user_id: int = Depends(get_user_id),
    user_service: UserService = Depends(
        get_user_service
    ),
) -> dict[str, str]:
    return await user_service.edit_user(update_user, current_user_id, user_id)


@router.delete(
    path="/{user_id}",
    response_model=dict[str, str]
)
async def delete_user(
    user_id: int,
    response: Response,
    authorize: AuthJWT = Depends(),
    current_user_id: int = Depends(get_user_id),
    user_service: UserService = Depends(
        get_user_service
    ),
) -> dict[str, str]:
    return await user_service.delete_user(
        response,
        authorize,
        current_user_id,
        user_id
    )
