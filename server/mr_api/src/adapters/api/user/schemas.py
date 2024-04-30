from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    dt: str
    first_name: str
    last_name: str
    email: str
    role: str
    is_premium: bool


class UpdateUser(BaseModel):
    first_name: str | None
    last_name: str | None
    email: EmailStr | None
