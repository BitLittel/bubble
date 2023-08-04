from pydantic import BaseModel
from datetime import datetime


class Music(BaseModel):
    track_id: int
    track_number: int | None
    track_name: str
    track_author: str
    track_genre: str
    track_cover: str
    track_path: str
    track_duration: str
    track_datetime_add: datetime
    user_id_add: int
