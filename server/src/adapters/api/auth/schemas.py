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

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "id": 1,
    #             "first_name": "John",
    #             "last_name": "Doe",
    #             "email": "john.doe@example.com",
    #             "access_token": "example_access_token",
    #             "refresh_token": "example_refresh_token"
    #         }
    #     }
