from dataclasses import dataclass


@dataclass
class City:
    id: int
    raw_name: str
    original_name: str
