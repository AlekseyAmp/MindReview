import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    EMAIL_USERNAME: str = os.environ["EMAIL_USERNAME"]
    EMAIL_PASSWORD: str = os.environ["EMAIL_PASSWORD"]
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587


settings = Settings()
