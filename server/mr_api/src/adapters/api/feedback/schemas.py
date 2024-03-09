from pydantic import BaseModel, EmailStr


class SendFeedback(BaseModel):
    email: EmailStr
    message: str


class ReplyFeedback(BaseModel):
    feedback_id: int
    response: str


class FeedbackResponse(BaseModel):
    id: int
    dt: str
    response_dt: str | None
    message: str
    response: str | None
    sender_email: str
    recipient_email: str


class FeedbacksResponse(BaseModel):
    answered: list[FeedbackResponse | None]
    unanswered: list[FeedbackResponse | None]
