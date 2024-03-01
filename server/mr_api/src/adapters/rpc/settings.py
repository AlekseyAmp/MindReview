import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    RABBITMQ_HOST: str = os.environ["RABBITMQ_HOST"]
    RABBITMQ_PORT: int = os.environ["RABBITMQ_PORT"]
    RABBITMQ_LOGIN: str = os.environ["RABBITMQ_LOGIN"]
    RABBITMQ_PASSWORD: str = os.environ["RABBITMQ_PASSWORD"]

    REVIEW_QUEUE_NAME: str = os.environ["REVIEW_QUEUE_NAME"]
    ANALYZE_QUEUE_NAME: str = os.environ["ANALYZE_QUEUE_NAME"]


settings = Settings()
