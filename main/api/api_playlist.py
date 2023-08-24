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
from main.schemas.playlist import ResponseAllPlayList, PlayListWithMusic
from main.utils.playlist import get_playlists_with_user_id, get_playlist_by_id
from main.schemas.user import UserRegular, UserLogin, UserSignUp
from main.utils.user import get_user_by_username, get_user_by_email, get_current_user, get_user_by_token_with_type


@main.get("/api/playlist", response_model=ResponseAllPlayList)
async def api_get_all_playlist(user: UserRegular = Depends(get_current_user)):
    get_user_all_playlist = await get_playlists_with_user_id(user.id)
    return get_user_all_playlist


@main.get("/api/playlist/{id_playlist}", response_model=PlayListWithMusic)
async def api_get_playlist_with_id(id_playlist: int, user: UserRegular = Depends(get_current_user)):
    # todo: добавить атрибуты для сортировки треков, по дате, но номеру трека, по длительности, по алфавиту
    get_playlist = await get_playlist_by_id(id_playlist, user.id)
    return get_playlist


# append default playlist id in liked_playlist array
# await query_execute(
#     query_text=f'update "Users" '
#                f'set liked_playlist = ('
#                f'select U.liked_playlist || {default_playlist.id} from "Users" as U where U.id = {get_new_user.id}'
#                f') where id = {get_new_user.id}',
#     fetch_all=False,
#     type_query='update'
# )
# # remove playlist id in liked_playlist array
# # update "Users"
# # set liked_playlist = (select
# #     array_remove(U.liked_playlist, 12)
# # from "Users" as U
# # where U.id = 11)
# # where id = 11
#
#
# @main.post("/api/add_playlist", response_model=DefaultResponse)
# async def api_add_playlist(id_playlist: int, user: UserRegular = Depends(get_current_user)):
#     get_user_all_playlist = await get_playlist_by_id(id_playlist)
#     print(get_user_all_playlist)
#     return {}
#
#
# @main.post("/api/edit_playlist/{id_playlist}", response_model=DefaultResponse)
# async def api_edit_playlist(id_playlist: int, user: UserRegular = Depends(get_current_user)):
#     get_user_all_playlist = await query_execute(
#         query_text=f'select * from "PlayLists" as PL where PL.user_id = {user.id}',
#         fetch_all=True,
#         type_query='read'
#     )
#     print(get_user_all_playlist)
#     return {}
#
#
# @main.post("/api/remove_playlist/{id_playlist}", response_model=DefaultResponse)
# async def api_remove_playlist(id_playlist: int, user: UserRegular = Depends(get_current_user)):
#     get_user_all_playlist = await query_execute(
#         query_text=f'select * from "PlayLists" as PL where PL.user_id = {user.id}',
#         fetch_all=True,
#         type_query='read'
#     )
#     print(get_user_all_playlist)
#     return {}
