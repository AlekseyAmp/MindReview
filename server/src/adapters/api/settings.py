import base64
import os

from dotenv import load_dotenv
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    JWT_PUBLIC_KEY: str = os.environ["JWT_PUBLIC_KEY"]
    JWT_PRIVATE_KEY: str = os.environ["JWT_PRIVATE_KEY"]
    JWT_ALGORITHM: str = os.environ["JWT_ALGORITHM"]
    REFRESH_TOKEN_EXPIRES_IN: int = os.environ["REFRESH_TOKEN_EXPIRES_IN"]
    ACCESS_TOKEN_EXPIRES_IN: int = os.environ["ACCESS_TOKEN_EXPIRES_IN"]

    authjwt_algorithm: str = JWT_ALGORITHM
    authjwt_decode_algorithms: list[str] = [JWT_ALGORITHM]
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_cookie_csrf_protect: bool = False

    authjwt_public_key: str = base64.b64decode(JWT_PUBLIC_KEY).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(
        JWT_PRIVATE_KEY
    ).decode('utf-8')


@AuthJWT.load_config
def get_config() -> Settings:
    return Settings()


settings = Settings()
