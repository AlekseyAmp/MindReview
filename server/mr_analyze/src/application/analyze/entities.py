from dataclasses import dataclass

from src.application.constants import Status


@dataclass
class EntryAnalyze:
    number: int
    raiting: float | None
    message: str
    sentiment: str
    keywords: list[str | None]
    author_gender: str | None
    author_age: float | None


@dataclass
class AnalyzeResults:
    entries_analyze: list[EntryAnalyze] | None
    full_analyze: dict | None
    status: Status
