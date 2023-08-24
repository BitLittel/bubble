from pydantic import BaseModel
from main.schemas.response import DefaultResponse
from main.schemas.music import Music


class Photo(BaseModel):
    path: str


class File(BaseModel):
    type: str
    file_data: Music | Photo


class FileResponse(DefaultResponse):
    data: File
