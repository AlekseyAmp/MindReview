from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogInput:
    dt: datetime
    level: str
    message: str


@dataclass
class LogReturn:
    id: int
    dt: datetime
    level: str
    message: str
