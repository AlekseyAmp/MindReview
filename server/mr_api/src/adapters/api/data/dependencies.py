from sqlalchemy.orm import Session

from fastapi import Depends

from src.adapters.database.repositories import DataRepository, UserRepository
from src.adapters.database.sa_session import get_session
from src.application.data.services import DataService


def get_data_repo(
    session: Session = Depends(get_session)
) -> DataRepository:
    return DataRepository(session)


def get_user_repo(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


def get_data_service(
    data_repo: DataRepository = Depends(get_data_repo),
    user_repo: UserRepository = Depends(get_user_repo)
) -> DataService:
    return DataService(
        data_repo,
        user_repo
    )
