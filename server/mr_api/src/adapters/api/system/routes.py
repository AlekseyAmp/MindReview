from fastapi import APIRouter, Depends

from src.adapters.api.system import schemas
from src.adapters.api.system.dependencies import get_system_service
from src.adapters.api.user.dependencies import get_user_id
from src.application.system.services import SystemService

router = APIRouter()


@router.get(
    path="/info",
    response_model=schemas.SystemInfoResponse
)
async def get_system_info(
    user_id: int = Depends(get_user_id),
    system_service: SystemService = Depends(
        get_system_service
    ),
) -> schemas.SystemInfoResponse:
    return await system_service.get_system_info(user_id)


@router.get(
    path="/logs",
    response_model=schemas.SystemInfoResponse
)
async def get_system_logs(
    user_id: int = Depends(get_user_id),
    system_service: SystemService = Depends(
        get_system_service
    ),
) -> schemas.SystemInfoResponse:
    return await system_service.get_system_logs(user_id)
