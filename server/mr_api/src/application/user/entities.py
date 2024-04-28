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
class UserUpdate:
    id: int
    first_name: str | None
    last_name: str | None
    email: str | None
    password: str | None


@dataclass
class UserInfo:
    role: str
    is_premium: bool
