from dataclasses import dataclass
from datetime import datetime


@dataclass
class FeedbackInput:
    user_id: int
    response_dt: datetime | None
    message: str
    response: str | None
    sender_email: str
    recipient_email: str


@dataclass
class FeedbackUpdate:
    id: int
    response_dt: datetime
    response: str


@dataclass
class FeedbackReturn:
    id: int
    dt: datetime
    response_dt: datetime | None
    message: str
    response: str | None
    sender_email: str
    recipient_email: str
