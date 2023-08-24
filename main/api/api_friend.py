# from pydantic import UUID4
from main import main
# import os
# from uuid import uuid4
# from datetime import datetime, timedelta
# from main.models.database import query_execute, hash_password
# from typing import BinaryIO
# from fastapi.responses import FileResponse, StreamingResponse
from fastapi import Depends, HTTPException, Response, Request, status
# from main import config
# from main.schemas.response import DefaultResponse
# from main.schemas.playlist import ResponseAllPlayList, PlayListWithMusic
# from main.utils.playlist import get_playlists_with_user_id, get_playlist_by_id
from main.schemas.user import UserRegular, UserLogin, UserSignUp
from main.utils.user import get_user_by_username, get_user_by_email, get_current_user, get_user_by_token_with_type


@main.get("/api/friends")
async def api_get_all_playlist(user: UserRegular = Depends(get_current_user)):
    print(user)
    return {
        'result': True,
        'message': 'Успех',
        'data': {
            'friends': []
        }
    }
