from pydantic import BaseModel
from main.schemas.response import DefaultResponse
from datetime import datetime
from main.schemas.music import Music


class PlayList(BaseModel):
    playlist_id: int
    playlist_name: str
    playlist_cover: str
    playlist_datetime_add: datetime
    can_edit: bool


class PlayListAndMusic(BaseModel):
    playlist: PlayList
    musics: list[Music] | list


class PlayListWithMusic(DefaultResponse):
    data: PlayListAndMusic


class ResponseAllPlayList(DefaultResponse):
    data: list[PlayList]
