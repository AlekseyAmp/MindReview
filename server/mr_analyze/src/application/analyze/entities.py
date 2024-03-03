from dataclasses import dataclass

from src.application.constants import Status


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
class AnalyzeResults:
    entries_analyze: list[EntryAnalyze] | None
    full_analyze: dict | None
    status: Status


@dataclass
class NLPResult(OtherInfo):
    sentiments: dict[int, tuple[str, float]]
    keywords: dict[int, list[str | None]]
