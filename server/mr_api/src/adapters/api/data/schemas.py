from datetime import datetime

from pydantic import BaseModel


class StopwordResponse(BaseModel):
    id: int
    dt: datetime
    word: str
    use: bool
