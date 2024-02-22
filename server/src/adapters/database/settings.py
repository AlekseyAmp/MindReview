import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    DB_HOST: str = os.environ["DB_HOST"]
    DB_USER: str = os.environ["DB_USER"]
    DB_PASSWORD: str = os.environ["DB_PASSWORD"]
    DB_NAME: str = os.environ["DB_NAME"]

    SQLALCHEMY_DB_URL: str = (
        "postgresql+psycopg2://"
        f"{DB_USER}:"
        f"{DB_PASSWORD}@"
        f"{DB_HOST}/"
        f"{DB_NAME}"
    )

    ALEMBIC_SCRIPT_LOCATION: str = 'src.adapters.database:alembic'
    ALEMBIC_VERSION_LOCATIONS: str = 'src.adapters.database:migrations'
    ALEMBIC_MIGRATION_FILENAME_TEMPLATE: str = (
        '%%(year)d_'
        '%%(month).2d_'
        '%%(day).2d_'
        '%%(hour).2d_'
        '%%(minute).2d_'
        '%%(second).2d_'
        '%%(slug)s'
    )


settings = Settings()
