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
    track_list: list[Music] | list
    current_track_number: int
    last_track_number: int


class PlayListWithMusic(DefaultResponse):
    data: PlayListAndMusic


class ResponseAllPlayList(DefaultResponse):
    data: list[PlayList]
