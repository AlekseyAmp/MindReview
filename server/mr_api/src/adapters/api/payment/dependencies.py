from sqlalchemy.orm import Session

from fastapi import Depends

from src.adapters.api.auth.token import TokenManager
from src.adapters.database.repositories import SystemRepository, UserRepository
from src.adapters.database.sa_session import get_session
from src.application.payment.services import PaymentService


def get_user_repo(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


def get_system_repo(
    session: Session = Depends(get_session)
) -> SystemRepository:
    return SystemRepository(session)


def get_token_manager() -> TokenManager:
    return TokenManager()


def get_payment_service(
    user_repo: UserRepository = Depends(get_user_repo),
    system_repo: SystemRepository = Depends(get_system_repo),
    token_manager: TokenManager = Depends(get_token_manager)
) -> PaymentService:
    return PaymentService(user_repo, system_repo, token_manager)
