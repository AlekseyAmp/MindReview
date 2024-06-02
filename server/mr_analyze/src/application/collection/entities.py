from dataclasses import dataclass
from datetime import datetime


@dataclass
class City:
    id: int
    raw_name: str
    original_name: str


@dataclass
class StopwordInput:
    dt: datetime
    word: str


@dataclass
class StopwordReturn(StopwordInput):
    id: int
    use: bool
