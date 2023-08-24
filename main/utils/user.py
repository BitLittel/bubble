from pydantic import UUID4
from datetime import datetime
from fastapi import Cookie
from main import config
from main.models.database import query_execute
from fastapi import HTTPException
from main.schemas.user import UserRegular


async def get_user_by_username(username: str) -> UserRegular | bool:
    user = await query_execute(
        query_text=f'select '
                   f'U.id, '
                   f'U.username, '
                   f'CONCAT(\'{config.API_IMAGE}\', U.avatar) as avatar, '
                   f'U.online,'
                   f'U.liked_playlist '
                   f'from "Users" as U '
                   f'where U.username = \'{username}\'',
        fetch_all=False,
        type_query='read'
    )
    if user is not None:
        return UserRegular(
            id=user.id,
            username=user.username,
            avatar=user.avatar,
            online=user.online,
            liked_playlist=user.liked_playlist
        )
    return False


async def get_user_by_email(email: str) -> UserRegular | bool:
    user = await query_execute(
        query_text=f'select '
                   f'U.id, '
                   f'U.username, '
                   f'CONCAT(\'{config.API_IMAGE}\', U.avatar) as avatar, '
                   f'U.online,'
                   f'U.liked_playlist '
                   f'from "Users" as U '
                   f'where U.email = \'{email}\'',
        fetch_all=False,
        type_query='read'
    )
    if user is not None:
        return UserRegular(
            id=user.id,
            username=user.username,
            avatar=user.avatar,
            online=user.online,
            liked_playlist=user.liked_playlist
        )
    return False


async def get_current_user(token=Cookie()):
    if token is not None or token != '':
        user = await get_user_by_token_with_type(token=token, type_token='regular')
        if user:
            return user
    raise HTTPException(status_code=401, detail="Unauthorized")


async def get_user_by_token_with_type(token: UUID4, type_token: str) -> UserRegular | bool:
    token_user = await query_execute(
        query_text=f'select * '
                   f'from "Tokens" as T '
                   f'where T.token = \'{token}\' and T.type = \'{type_token}\' '
                   f'and T.expires > \'{datetime.now()}\'',
        fetch_all=False,
        type_query='read'
    )
    if token_user is not None:
        user = await query_execute(
            query_text=f'select '
                       f'U.id, '
                       f'U.username, '
                       f'CONCAT(\'{config.API_IMAGE}\', U.avatar) as avatar, '
                       f'U.online,'
                       f'U.liked_playlist '
                       f'from "Users" as U '
                       f'where U.id = {token_user.user_id}',
            fetch_all=False,
            type_query='read'
        )
        if type_token == 'activate':
            await query_execute(
                query_text=f'delete from "Tokens" as T where T.token = \'{token}\'',
                fetch_all=False,
                type_query='delete'
            )
        return UserRegular(
            id=user.id,
            username=user.username,
            avatar=user.avatar,
            online=user.online,
            liked_playlist=user.liked_playlist
        )
    return False
