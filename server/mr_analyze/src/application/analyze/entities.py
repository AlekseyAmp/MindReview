from dataclasses import dataclass

from src.application.constants import Status


@dataclass
class EntryAnalyze:
    number: int
    message: str
    sentiment: str
    keywords: list[str | None]
    author_gender: str
    author_age: int | None


@dataclass
class AnalyzeResults:
    entries_analyze: list[EntryAnalyze] | None
    full_analyze: dict | None
    status: Status
