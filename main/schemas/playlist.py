from pydantic import BaseModel
from main.schemas.response import DefaultResponse
from datetime import datetime
from main.schemas.music import Music


class PlayList(BaseModel):
    id: int
    name: str
    cover: str
    datetime_add: datetime
    can_edit: bool


class PlayListAndMusic(BaseModel):
    playlist: PlayList
    track_list: dict[int, Music]
    current_track: dict[int, Music]
    track_count: int


class PlayListWithMusic(DefaultResponse):
    data: PlayListAndMusic


class ResponseAllPlayList(DefaultResponse):
    data: list[PlayList]
