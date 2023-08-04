from pydantic import UUID4
from main import main
import os
from uuid import uuid4
from datetime import datetime, timedelta
from main.models.database import query_execute, hash_password
from typing import BinaryIO
from fastapi.responses import FileResponse, StreamingResponse
from fastapi import Depends, HTTPException, Response, Request, status
from main import config
from main.schemas.response import DefaultResponse
from main.schemas.user import UserRegular, UserLogin, UserSignUp
from main.utils.user import get_user_by_username, get_user_by_email, get_current_user, get_user_by_token_with_type

# todo: Займёмся плейлистами и выдачей треков


@main.get("/api/music_download")
def api_music_download():
    return FileResponse(path='data.xlsx', filename='Статистика покупок.xlsx', media_type='multipart/form-data')


def send_bytes_range_requests(
    file_obj: BinaryIO, start: int, end: int, chunk_size: int = 10_000
):
    """Send a file in chunks using Range Requests specification RFC7233

    `start` and `end` parameters are inclusive due to specification
    """
    with file_obj as f:
        f.seek(start)
        while (pos := f.tell()) <= end:
            read_size = min(chunk_size, end + 1 - pos)
            yield f.read(read_size)


def _get_range_header(range_header: str, file_size: int) -> tuple[int, int]:
    def _invalid_range():
        return HTTPException(
            status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail=f"Invalid request range (Range:{range_header!r})",
        )

    try:
        h = range_header.replace("bytes=", "").split("-")
        start = int(h[0]) if h[0] != "" else 0
        end = int(h[1]) if h[1] != "" else file_size - 1
    except ValueError:
        raise _invalid_range()

    if start > end or start < 0 or end > file_size - 1:
        raise _invalid_range()
    return start, end


def range_requests_response(
    request: Request, file_path: str, content_type: str
):
    """Returns StreamingResponse using Range Requests of a given file"""

    file_size = os.stat(file_path).st_size
    range_header = request.headers.get("range")

    headers = {
        "content-type": content_type,
        "Connection": "keep-alive",
        "Keep-Alive": "timeout=60",
        "accept-ranges": "bytes",
        "content-encoding": "identity",
        "content-length": str(file_size),
        "access-control-expose-headers": (
            "content-type, accept-ranges, content-length, "
            "content-range, content-encoding"
        ),
    }
    start = 0
    end = file_size - 1
    status_code = status.HTTP_200_OK

    if range_header is not None:
        start, end = _get_range_header(range_header, file_size)
        size = end - start + 1
        headers["content-length"] = str(size)
        headers["content-range"] = f"bytes {start}-{end}/{file_size}"
        status_code = status.HTTP_206_PARTIAL_CONTENT

    return StreamingResponse(
        send_bytes_range_requests(open(file_path, mode="rb"), start, end),
        headers=headers,
        status_code=status_code,
    )


@main.get("/api/music/{id_music}")
async def api_get_music(id_music: int, request: Request):
    # todo: тут будем из базы брать название трека uuid и его подставлять по пути stored_file/musics/dsfsd-sdf-sdfsd.mp3
    if id_music != 1:  # Это на время теста, позже уберёться нахуй
        get_music = await query_execute(
            query_text=f'select * from "Musics" as M where M.id = {id_music}',
            fetch_all=False,
            type_query='read'
        )
        if get_music is None:
            raise HTTPException(404, detail="Трек не найден")
        file_path = os.path.join(config.MUSICS_FOLDER, get_music.filename)
    else:
        file_path = os.path.join(config.MAIN_PATH, "static", "music", "1.mp3")
    return range_requests_response(
        request, file_path=file_path, content_type="audio/mpeg"
    )


@main.get("/api/music_list_test")
async def api_music_list_test():
    test_dict = {
        "result": True,
        "first_track_number": 1,
        "last_track_number": 4,
        "track_list": [
            {
                "track_id": 1,
                "track_number": 1,
                "track_name": "1",
                "track_author": "Bones",
                "track_duration": "3:20",
                "track_cover": f"{config.MAIN_URL}/api/image/1",
                "track_path": f"{config.MAIN_URL}/api/music/1"
            },
            {
                "track_id": 2,
                "track_number": 2,
                "track_name": "2",
                "track_author": "Bones",
                "track_duration": "3:20",
                "track_cover": f"{config.MAIN_URL}/api/image/1",
                "track_path": f"{config.MAIN_URL}/static/music/2.mp3"
            },
            {
                "track_id": 3,
                "track_number": 3,
                "track_name": "3",
                "track_author": "Bones",
                "track_duration": "3:20",
                "track_cover": f"{config.MAIN_URL}/api/image/3",
                "track_path": f"{config.MAIN_URL}/api/music/7"
            },
            {
                "track_id": 4,
                "track_number": 4,
                "track_name": "4",
                "track_author": "Bones",
                "track_duration": "3:20",
                "track_cover": f"{config.MAIN_URL}/api/image/1",
                "track_path": f"{config.MAIN_URL}/api/music/4"
            },
        ]
    }
    return test_dict

# todo: Изучить вопрос с FileResponse и понять какие есть ещё media_type
