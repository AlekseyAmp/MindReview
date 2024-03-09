from sqlalchemy.orm import Session

from fastapi import Depends

from src.adapters.database.repositories import (
    FeedbackRepository,
    UserRepository,
)
from src.adapters.database.sa_session import get_session
from src.adapters.email.sender import MailSender
from src.application.feedback.services import FeedbackService


def get_feedback_repo(
    session: Session = Depends(get_session)
) -> FeedbackRepository:
    return FeedbackRepository(session)


def get_user_repo(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


def get_mail_sender() -> MailSender:
    return MailSender()


def get_feedback_service(
    feedback_repo: FeedbackRepository = Depends(get_feedback_repo),
    user_repo: UserRepository = Depends(get_user_repo),
    mail_sender: MailSender = Depends(get_mail_sender)
) -> FeedbackService:
    return FeedbackService(
        feedback_repo,
        user_repo,
        mail_sender
    )
