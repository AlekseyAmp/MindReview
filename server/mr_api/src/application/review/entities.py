from dataclasses import dataclass
from datetime import datetime

from src.application.constants import Status


@dataclass
class AnalyzeInput:
    user_id: int
    dt: datetime
    source_type: str
    source_url: str | None
    entries_analyze: list[dict] | None
    full_analyze: dict | None
    status: Status


@dataclass
class AnalyzeReturn:
    id: int
    dt: datetime
    source_type: str
    source_url: str | None
    entries_analyze: list[dict] | None
    full_analyze: dict | None
    status: Status


@dataclass
class ReviewTemplate:
    number: int
    message: str
    author: str | None = None
    raiting: float | None = None
    country: str | None = None
    city: str | None = None
