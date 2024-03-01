from pydantic import BaseModel

from src.application.constants import Status


class AnalyzeResponse(BaseModel):
    id: int | None
    dt: str
    source_type: str
    source_url: str | None
    entries_analyze: list[dict] | None
    full_analyze: dict | None
    status: Status


class TestReviews(BaseModel):
    reviews: list[str]
