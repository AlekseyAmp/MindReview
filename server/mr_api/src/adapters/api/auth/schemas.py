from pydantic import BaseModel


class AuthUserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class CreateUser(AuthUserBase):
    password: str


class LoginUser(BaseModel):
    email: str
    password: str


class AuthResponse(AuthUserBase):
    id: int
    access_token: str
    refresh_token: str
