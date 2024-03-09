from dataclasses import dataclass
from datetime import datetime

from src.application.constants import UserRole


@dataclass
class User:
    id: int
    dt: datetime
    first_name: str
    last_name: str
    email: str
    password: str
    role: UserRole
    is_premium: bool


@dataclass
class UserInfo:
    role: UserRole
    is_premium: bool
