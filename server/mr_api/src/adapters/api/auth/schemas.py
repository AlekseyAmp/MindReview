from pydantic import BaseModel, EmailStr


class AuthUserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class CreateUser(AuthUserBase):
    password: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(AuthUserBase):
    id: int
    access_token: str
    refresh_token: str
