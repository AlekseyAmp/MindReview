from pydantic import BaseModel


class StopwordResponse(BaseModel):
    id: int
    dt: str
    word: str
    use: bool
