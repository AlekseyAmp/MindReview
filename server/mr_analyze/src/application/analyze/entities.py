from dataclasses import dataclass
from datetime import datetime

from src.application.constants import Status


@dataclass
class AnalyzeInput:
    user_id: int
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
class OtherInfo:
    cities: list[str | None]
    years: list[int | None]


@dataclass
class EntryAnalyze:
    number: int
    raiting: float | None
    message: str
    sentiment: str
    keywords: list[str | None]
    other_info: OtherInfo


@dataclass
class FullAnalyze:
    keywords_cloud: dict[str, int] | None
    sentiments_data: dict[str, dict[str | dict] | int]
    keyword_sentiment_counts: dict[str, dict[str, int]] | None
    geographical_map: dict[str, int] | None


@dataclass
class AnalyzeResults:
    entries_analyze: list[EntryAnalyze] | None
    full_analyze: dict | None
    status: Status


@dataclass
class NLPResult(OtherInfo):
    sentiments: dict[int, tuple[str, float]]
    keywords: dict[int, list[str | None]]
