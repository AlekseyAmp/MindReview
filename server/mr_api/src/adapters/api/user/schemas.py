from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    dt: str
    first_name: str
    last_name: str
    email: str
    role: str
    is_premium: bool


class UsersResponse(BaseModel):
    users: list[UserResponse | None]
