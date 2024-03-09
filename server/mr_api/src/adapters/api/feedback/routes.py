from fastapi import APIRouter, Depends

from src.adapters.api.feedback import schemas
from src.adapters.api.feedback.dependencies import get_feedback_service
from src.adapters.api.user.dependencies import get_user_id
from src.application.feedback.services import FeedbackService

router = APIRouter()


@router.post(path="/send", response_model=dict[str, str])
async def send_feedback(
    feedback: schemas.SendFeedback,
    user_id: int = Depends(get_user_id),
    feedback_service: FeedbackService = Depends(
        get_feedback_service
    ),
) -> dict[str, str]:
    return await feedback_service.send_feedback(feedback, user_id)


@router.post(path="/reply", response_model=dict[str, str])
async def reply_feedback(
    reply: schemas.ReplyFeedback,
    user_id: int = Depends(get_user_id),
    feedback_service: FeedbackService = Depends(
        get_feedback_service
    ),
) -> dict[str, str]:
    return await feedback_service.reply_feedback(reply, user_id)


@router.get(
    path="/get_all",
    response_model=schemas.FeedbacksResponse
)
async def get_all_feedbacks(
    user_id: int = Depends(get_user_id),
    feedback_service: FeedbackService = Depends(
        get_feedback_service
    ),
) -> schemas.FeedbacksResponse:
    return await feedback_service.get_all_feedbacks(user_id)
