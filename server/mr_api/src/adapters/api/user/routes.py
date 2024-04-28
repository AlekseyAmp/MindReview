from fastapi import APIRouter, Depends

from src.adapters.api.user import schemas
from src.adapters.api.user.dependencies import get_user_id, get_user_service
from src.application.user.services import UserService

router = APIRouter()


@router.get(
    path="/get/{user_id}",
    response_model=schemas.UserResponse
)
async def get_user(
    user_id: int,
    current_user_id: int = Depends(get_user_id),
    user_service: UserService = Depends(
        get_user_service
    ),
) -> schemas.UserResponse:
    return await user_service.get_user(user_id)


@router.get(
    path="/get_all",
    response_model=schemas.UsersResponse
)
async def get_all_users(
    user_id: int = Depends(get_user_id),
    user_service: UserService = Depends(
        get_user_service
    ),
) -> schemas.UsersResponse:
    return await user_service.get_all_users(user_id)
