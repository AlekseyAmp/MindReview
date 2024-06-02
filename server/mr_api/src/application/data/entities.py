from dataclasses import dataclass
from datetime import datetime


@dataclass
class StopwordReturn:
    id: int
    dt: datetime
    word: str
    use: bool
