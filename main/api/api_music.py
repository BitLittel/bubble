from pydantic import UUID4
from main import main
from uuid import uuid4
from datetime import datetime, timedelta
from main.models.database import query_execute, hash_password
from fastapi.responses import FileResponse
from fastapi import Depends, HTTPException, Response
from main import config
from main.schemas.response import DefaultResponse
from main.schemas.user import UserRegular, UserLogin, UserSignUp
from main.utils.user import get_user_by_username, get_user_by_email, get_current_user, get_user_by_token_with_type


@main.get("/api/music_download")
def api_music_download():
    return FileResponse(path='data.xlsx', filename='Статистика покупок.xlsx', media_type='multipart/form-data')


@main.get("/api/music_list_test")
def api_music_list_test():
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
                "track_cover": f"{config.MAIN_URL}/static/img/default_img.jpg",
                "track_path": f"{config.MAIN_URL}/static/music/1.mp3"
            },
            {
                "track_id": 2,
                "track_number": 2,
                "track_name": "2",
                "track_author": "Bones",
                "track_duration": "3:20",
                "track_cover": f"{config.MAIN_URL}/static/img/default_img.jpg",
                "track_path": f"{config.MAIN_URL}/static/music/2.mp3"
            },
            {
                "track_id": 3,
                "track_number": 3,
                "track_name": "3",
                "track_author": "Bones",
                "track_duration": "3:20",
                "track_cover": f"{config.MAIN_URL}/static/img/default_img.jpg",
                "track_path": f"{config.MAIN_URL}/static/music/3.mp3"
            },
            {
                "track_id": 4,
                "track_number": 4,
                "track_name": "4",
                "track_author": "Bones",
                "track_duration": "3:20",
                "track_cover": f"{config.MAIN_URL}/static/img/default_img.jpg",
                "track_path": f"{config.MAIN_URL}/static/music/4.mp3"
            },
        ]
    }
    return test_dict

# todo: Изучить вопрос с FileResponse и понять какие есть ещё media_type
