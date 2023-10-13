from pydantic import BaseModel
from datetime import datetime


class Music(BaseModel):
    id: int
    name: str
    author: str
    genre: str | None
    cover: str
    path: str
    duration: str
    datetime_add: datetime
    can_edit: bool
