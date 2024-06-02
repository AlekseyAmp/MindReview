from fastapi import APIRouter, Depends

from src.adapters.api.data import schemas
from src.adapters.api.data.dependencies import get_data_service
from src.adapters.api.user.dependencies import get_user_id
from src.application.data.services import DataService

router = APIRouter()


@router.get(
    path="/stopwords",
    response_model=list[schemas.StopwordResponse]
)
async def get_all_stopwords(
    user_id: int = Depends(get_user_id),
    data_service: DataService = Depends(
        get_data_service
    )
) -> list[schemas.StopwordResponse]:
    return await data_service.get_all_stopwords(user_id)


@router.patch(path="/stopwords/{stopword_id}", response_model=dict[str, str])
async def set_stopword_is_use(
    stopword_id: int,
    user_id: int = Depends(get_user_id),
    data_service: DataService = Depends(
        get_data_service
    )
) -> dict[str, str]:
    return await data_service.set_stopword_is_use(stopword_id, user_id)


@router.delete(path="/stopwords/{stopword_id}", response_model=dict[str, str])
async def delete_stopword(
    stopword_id: int,
    user_id: int = Depends(get_user_id),
    data_service: DataService = Depends(
        get_data_service
    )
) -> dict[str, str]:
    return await data_service.delete_stopword(stopword_id, user_id)
