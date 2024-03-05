from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    dt: datetime
    first_name: str
    last_name: str
    email: str
    password: str
    role: str
    is_premium: bool


@dataclass
class UserIsPremium:
    is_premium: bool
